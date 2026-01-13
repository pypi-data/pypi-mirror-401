"""Documentation agent for large-scale code analysis."""

import os
import json
import asyncio
from pathlib import Path
from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage
from coding_agent_plugin.agents.base_agent import BaseAgent
from coding_agent_plugin.context.project_context import ProjectContext
from coding_agent_plugin.core.logging import get_logger

class DocumentationAgent(BaseAgent):
    """
    Agent responsible for analyzing codebases and generating documentation 
    using a Map-Reduce file-based approach for scalability.
    """
    
    def __init__(self, name: str = "documentation"):
        super().__init__(name)
        self.logger = get_logger(f"agent.{name}")

    async def execute(self, task: Any) -> Dict[str, Any]:
        """
        Execute the documentation task.
        
        Expected task keys:
            project_id: str
            project_path: str (optional, will be resolved if not present)
            topic: str (optional, for specific feature documentation)
            force: bool (optional, force re-indexing)
            refine_path: str (optional, path to existing file to refine)
            instruction: str (optional, instruction for refinement)
        """
        project_id = task.get("project_id")
        topic = task.get("topic")
        force_reindex = task.get("force", False)
        
        # Refinement Support
        refine_path = task.get("refine_path")
        instruction = task.get("instruction")
        
        if refine_path and instruction:
            return await self._refine_artifact(refine_path, instruction)

        self.logger.info(f"Starting analysis for project: {project_id}")
        if topic:
             self.logger.info(f"Focusing analysis on topic: {topic}")
        
        # Setup context
        project_path = task.get("project_path")
        
        if not project_path and project_id:
            from coding_agent_plugin.managers import ProjectManager
            pm = ProjectManager()
            project = pm.get_project(project_id)
            if project:
                project_path = project.get("storage_path")
                
        if not project_path:
            project_path = os.getcwd()
            
        context = ProjectContext(project_path)
        if not context.load_project():
             return {"status": "failed", "error": "Failed to load project"}
             
        # Create .agent_context directory if needed
        context_dir = Path(project_path) / ".agent_context"
        context_dir.mkdir(parents=True, exist_ok=True)
        
        memory_file = context_dir / "knowledge_graph.jsonl"
        
        # MAP PHASE: Index files
        self.logger.info("🗺️  Phase 1: Mapping (Indexing Files)")
        await self._map_phase(context, memory_file, force_reindex)
        
        # REDUCE PHASE: Synthesize documentation
        self.logger.info("🔥 Phase 2: Refine (Synthesis)")
        docs_generated = await self._reduce_phase(memory_file, Path(project_path) / "docs", project_id, topic)
        
        return {"status": "completed", "docs": docs_generated}

    async def _refine_artifact(self, path_str: str, instruction: str) -> Dict[str, Any]:
        """Refine an existing artifact based on user instruction."""
        path = Path(path_str)
        if not path.exists():
            return {"status": "failed", "error": f"File not found: {path}"}
            
        self.logger.info(f"🎨 Refining artifact: {path.name}")
        
        content = path.read_text(encoding='utf-8')
        llm = self.get_llm()
        
        prompt = f"""
        You are an expert technical editor and code documenter.
        
        TASK: Update the following file content based on the user's instruction.
        
        FILE: {path.name}
        INSTRUCTION: {instruction}
        
        CONTENT START:
        {content[:60000]} 
        CONTENT END.
        
        Output ONLY the updated content. Do not encompass in markdown code blocks unless the file itself is markdown/code.
        If it's a mermaid file, output pure mermaid code.
        """
        
        from langchain_core.messages import HumanMessage
        response = await llm.ainvoke([HumanMessage(content=prompt)])
        
        updated_content = response.content
        
        # Strip markdown fences if LLM added them unnecessarily for non-markdown files (e.g. mermaid)
        if path.suffix == '.mermaid':
            updated_content = updated_content.replace('```mermaid', '').replace('```', '').strip()
            
        path.write_text(updated_content, encoding='utf-8')
        
        return {
            "status": "completed", 
            "message": f"Refined {path.name}",
            "docs": [str(path)]
        }

    def _compute_file_hash(self, content: str) -> str:
        """Compute MD5 hash of content for change detection."""
        import hashlib
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    async def _map_phase(self, context: ProjectContext, output_file: Path, force_reindex: bool = False):
        """Streaming analysis of files with incremental updates."""
        from langchain_core.messages import SystemMessage, HumanMessage
        
        llm = self.get_llm()
        
        # Load existing index if available
        existing_index = {}
        if output_file.exists() and not force_reindex:
            with open(output_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if 'path' in entry:
                            existing_index[entry['path']] = entry
                    except: pass
        
        # Prepare new index (in-memory first for atomic update, or streaming rewrite)
        # For safety and append-log style, we'll rewrite the file at the end or use a temp file.
        # Here we'll build a 'new_state' list.
        new_state = []
            
        file_count = 0
        reused_count = 0
        analyzed_count = 0
        
        files_iterator = list(context.file_iterator()) # Materialize to progress tracking if needed
        
        for rel_path, content in files_iterator:
            file_count += 1
            if file_count % 10 == 0:
                self.logger.info(f"  Processed {file_count} files...")
            
            # Simple heuristic
            if not rel_path.endswith(('.py', '.js', '.ts', '.tsx', '.go', '.java', '.cpp')):
                continue
                
            current_hash = self._compute_file_hash(content)
            
            # CHECK CACHE
            cached_entry = existing_index.get(rel_path)
            
            if (not force_reindex and 
                cached_entry and 
                cached_entry.get('hash') == current_hash):
                
                # Reuse existing entry
                new_state.append(cached_entry)
                reused_count += 1
                continue
                
            # If we are here, we need to analyze
            analyzed_count += 1
            prompt = f"""
            Analyze this code file: {rel_path}
            
            Return a JSON object with:
            1. "summary": Brief 1-sentence description.
            2. "imports": List of imported modules/files.
            3. "exports": List of main classes/functions defined.
            
            Code snippet (truncated):
            {content[:2000]} 
            """
            
            try:
                response = await llm.ainvoke([
                    SystemMessage(content="You are a code analyzer. Output JSON only."),
                    HumanMessage(content=prompt)
                ])
                
                import re
                json_match = re.search(r'\{.*\}', response.content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    data['path'] = rel_path
                    data['hash'] = current_hash # Store hash
                    new_state.append(data)
                        
            except Exception as e:
                self.logger.warning(f"Failed to analyze {rel_path}: {e}")
        
        # Write updated knowledge graph
        self.logger.info(f"  Analysis complete: {analyzed_count} analyzed, {reused_count} cached.")
        with open(output_file, 'w') as f:
            for item in new_state:
                f.write(json.dumps(item) + "\n")

    async def _reduce_phase(self, memory_file: Path, docs_dir: Path, project_id: str, topic: str = None) -> List[str]:
        """Synthesize findings into documentation."""
        docs_dir.mkdir(exist_ok=True)
        
        # Load all knowledge
        knowledge = []
        if memory_file.exists():
            with open(memory_file, 'r') as f:
                for line in f:
                    try:
                        knowledge.append(json.loads(line))
                    except: pass
        
        if not knowledge:
            self.logger.warning("No knowledge gathered.")
            return []
            
        generated_files = []

        # If topic provided, generate SPECIALIZED DOC only
        if topic:
             topic_slug = topic.replace(" ", "_").lower()
             topic_path = docs_dir / f"{topic_slug}.md"
             await self._generate_topic_doc(knowledge, topic_path, project_id, topic)
             generated_files.append(str(topic_path))
             return generated_files

        # OTHERWISE: Generate STANDARD DOCS (Architecture + Overview)
        
        # Generare Architecture Diagram (Mermaid)
        mermaid_path = docs_dir / "architecture.mermaid"
        await self._generate_mermaid(knowledge, mermaid_path)
        generated_files.append(str(mermaid_path))
        
        # Generate End-to-End Overview
        overview_path = docs_dir / "OVERVIEW.md"
        await self._generate_overview(knowledge, overview_path, project_id)
        generated_files.append(str(overview_path))
        
        return generated_files

    async def _generate_mermaid(self, knowledge: List[Dict], output_path: Path):
        """Generate dependency graph."""
        
        # 1. Build a map of internal modules
        internal_modules = {}
        file_map = {} # path -> node_id
        
        # Subgraphs storage: category -> list of lines
        subgraphs = {}
        
        # Track defined nodes to avoid duplicates
        defined_nodes = set()
        
        for item in knowledge:
            path = item.get('path', '')
            if not path: continue
            
            # Exclude tests, examples, and __init__.py files
            if any(x in path for x in ["tests/", "examples/", "conftest.py", "__init__.py"]) or path.startswith("test_"):
                continue
            
            # Create a unique node ID based on path components
            parts = Path(path).with_suffix('').parts
            
            # Simplify ID by removing common prefixes
            filtered_parts = [p for p in parts if p not in ('src', 'coding_agent_plugin', '.')]
            node_id = "_".join(filtered_parts).replace('-', '_').replace('.', '_')
            
            # Fallback
            if not node_id:
                node_id = Path(path).stem
                
            if node_id[0].isdigit():
                node_id = "f_" + node_id

            file_map[path] = node_id
            
            # Map module path
            module_key = ""
            if 'src' in parts:
                idx = parts.index('src')
                module_key = ".".join(parts[idx+1:])
                internal_modules[module_key] = node_id
            else:
                module_key = ".".join(parts)
                internal_modules[module_key] = node_id
            
            # Determine subgraph category
            possible_categories = ['agents', 'core', 'services', 'cli', 'managers', 'integrations', 'utils', 'models', 'context', 'acp', 'mcp', 'repositories', 'schemas', 'benchmarks', 'ui']
            category = "Other"
            
            for cat in possible_categories:
                if cat in filtered_parts:
                    category = cat.capitalize()
                    break
            
            if category not in subgraphs:
                subgraphs[category] = []
                
            if node_id not in defined_nodes:
                # Add node with styling class based on category
                subgraphs[category].append(f"    {node_id}[{Path(path).name}]:::{category}")
                defined_nodes.add(node_id)
                
        # Construct Mermaid content
        lines = ["graph LR"]
        
        # Add Styles
        lines.append("    %% Styles")
        lines.append("    classDef Agents fill:#ffeba1,stroke:#d4b106,color:#333;")
        lines.append("    classDef Core fill:#e1f5fe,stroke:#0288d1,color:#333;")
        lines.append("    classDef Services fill:#e8f5e9,stroke:#388e3c,color:#333;")
        lines.append("    classDef Managers fill:#f3e5f5,stroke:#8e24aa,color:#333;")
        lines.append("    classDef Cli fill:#fbe9e7,stroke:#d84315,color:#333;")
        lines.append("    classDef Acp fill:#e0f2f1,stroke:#009688,color:#333;")
        lines.append("    classDef Mcp fill:#fce4ec,stroke:#c2185b,color:#333;")
        lines.append("    classDef Utils fill:#f1f8e9,stroke:#689f38,color:#333;")
        lines.append("    classDef Repositories fill:#fff9c4,stroke:#fbc02d,color:#333;")
        lines.append("    classDef Schemas fill:#e0f7fa,stroke:#00acc1,color:#333;")
        lines.append("    classDef category fill:#fff,stroke:#333,color:#333;")
        
        # Sort subgraphs for stability
        for cat in sorted(subgraphs.keys()):
            lines.append(f"    subgraph {cat}")
            lines.extend(subgraphs[cat])
            lines.append("    end")
            
        # 2. Draw edges
        edges = set()
        
        for item in knowledge:
            path = item.get('path', '')
            if not path: continue
            
            source_id = file_map.get(path)
            if not source_id: continue
            
            imports = item.get('imports', [])
            for imp in imports:
                # Resolve import
                target_id = None
                
                # Exact match
                if imp in internal_modules:
                    target_id = internal_modules[imp]
                
                # Parent match
                elif "." in imp:
                    parent = imp.rsplit('.', 1)[0]
                    if parent in internal_modules:
                        target_id = internal_modules[parent]
                    elif "." in parent:
                        grandparent = parent.rsplit('.', 1)[0]
                        if grandparent in internal_modules:
                            target_id = internal_modules[grandparent]
                
                # If found, not self-loop, and target is in defined nodes (not a filtered test)
                if target_id and target_id != source_id and target_id in defined_nodes:
                     edge = f"    {source_id} --> {target_id}"
                     if edge not in edges:
                         lines.append(edge)
                         edges.add(edge)
                     
        with open(output_path, 'w') as f:
            f.write("\n".join(lines))
            
    async def _generate_overview(self, knowledge: List[Dict], output_path: Path, project_id: str):
        """Generate textual overview."""
        llm = self.get_llm()
        
        # Create a summary of summaries (Context reduction)
        system_summary = "\n".join([f"- {k['path']}: {k.get('summary', 'No summary')}" for k in knowledge])
        
        prompt = f"""
        Here is a list of all files in project '{project_id}' and their summaries:
        
        {system_summary[:50000]} # Limit token usage
        
        Write a comprehensive End-to-End Documentation (OVERVIEW.md) that explains:
        1. The purpose of the project.
        2. Key components and how they interact.
        3. The data flow.
        """
        
        response = await llm.ainvoke([
            HumanMessage(content=prompt)
        ])
        
        with open(output_path, 'w') as f:
            f.write(response.content)

    async def _generate_topic_doc(self, knowledge: List[Dict], output_path: Path, project_id: str, topic: str):
        """Generate specific topic documentation."""
        from langchain_core.messages import HumanMessage
        llm = self.get_llm()
        
        # Create a summary of summaries 
        system_summary = "\n".join([f"- {k['path']}: {k.get('summary', 'No summary')}" for k in knowledge])
        
        prompt = f"""
        Here is a list of all files in project '{project_id}':
        
        {system_summary[:60000]} 
        
        USER REQUEST: generate documentation specifically about "{topic}".
        
        Write a detailed Markdown document ({output_path.name}) that covers:
        1. What "{topic}" is in this project.
        2. Which files implement it.
        3. Detailed explanation of the logic/flow related to "{topic}".
        """
        
        response = await llm.ainvoke([
            HumanMessage(content=prompt)
        ])
        
        with open(output_path, 'w') as f:
            f.write(response.content)
