"""Planning agent for task planning and workflow design using LangChain."""

import json
import re
from typing import List, Dict, Any
from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.services.prompt_service import PromptService


class PlanningAgent(BaseAgent):
    """Agent responsible for task planning and workflow design."""

    def __init__(self, name: str = "planning", model: str = None):
        super().__init__(name, model)
        self.pm = ProjectManager()
        self.model = self.get_llm()

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the planning task."""
        user_prompt = task.get("user_prompt")
        project_id = task.get("project_id")

        if not user_prompt or not project_id:
            raise ValueError("Missing user_prompt or project_id")

        self.log(f"Executing planning task: {user_prompt}")
        
        # Get existing files
        existing_files = self.pm.list_files(project_id)
        
        # Dynamic Context Discovery via MCP
        # 1. Use LLM to identify relevant search queries (Semantic Search)
        keywords = await self.identify_search_queries(user_prompt, existing_files)
        if keywords:
            self.log(f"LLM identified search queries: {keywords}")
        else:
             # Fallback to naive if LLM fails
            ignore_words = {"create", "add", "update", "delete", "remove", "fix", "implement", "the", "a", "an", "for", "in", "to", "not", "coming", "working", "is"}
            keywords = [w for w in user_prompt.replace(".", " ").split() if w.lower() not in ignore_words and len(w) > 3]
        
        # 2. Use MCP Search Tool to find relevant files
        found_context = []
        for kw in keywords[:3]: # Limit to top 3 keywords
             search_results = await self.get_project_context(project_id, query=kw)
             if search_results and "No matches found" not in search_results:
                 found_context.append(f"Search results for '{kw}':\n{search_results[:500]}...") # Truncate for context window
        
        context_str = "\n".join(found_context)
        if context_str:
            self.log(f"Discovered relevant context via MCP:\n{context_str}")

        workflow = await self.plan(user_prompt, existing_files, context_str)
        
        self.save_plan(project_id, workflow)
        
        return {"workflow": workflow}

    async def plan(self, user_input: str, existing_files: List[str] = None, discovered_context: str = "") -> Dict[str, Any]:
        """Plan the workflow for the user's input using LangChain."""
        self.log(f"Planning workflow for: {user_input}")
        
        files_context = ""
        if discovered_context:
            files_context += f"\n\nDiscovered Code Context (via MCP Search):\n{discovered_context}\n"
            
        if existing_files:
            files_context += f"\nExisting Project Files:\n{', '.join(existing_files)}\n"
            files_context += """
IMPORTANT GUIDELINES FOR EXISTING PROJECTS:
1. ANALYZE the existing file structure and naming conventions carefully.
2. FOLLOW the established patterns for new modules (e.g., if 'routers.py' is used for routes in one module, use 'routers.py' for new modules too).
3. DO NOT create redundant files if shared utilities already exist (e.g., use existing database/crud.py if applicable).
4. INTEGRATE new files seamlessly into the existing architecture (e.g., ensure main.py imports new routers correctly).
5. MAINTAIN consistency in coding style and structure.
"""
        
        system_prompt = SystemMessage(content=PromptService.get_planning_system_prompt(files_context))
        input_prompt = HumanMessage(content=f"Request: {user_input}")
        
        messages = [system_prompt, input_prompt]
        # Call LLM with retry
        response = await self.retry_operation(self.model.ainvoke, messages)
        content = response.content
        
        # Robust JSON extraction
        try:
            # Find the first { and the last }
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                json_str = match.group(0)
                plan = json.loads(json_str)
                return plan
            else:
                raise ValueError("No JSON object found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            self.log(f"Failed to decode JSON plan: {e}")
            return {"error": str(e), "raw_content": content, "architecture": {}, "tasks": []}

    def save_plan(self, project_id: str, workflow: Dict[str, Any]) -> None:
        """Save planning details to a file."""
        # Resolve project path using ProjectManager
        project = self.pm.get_project(project_id)
        if not project:
            self.log(f"Project {project_id} not found, cannot save plan")
            return
            
        storage_path = Path(project["storage_path"])
        context_dir = storage_path / ".agentic"
        context_dir.mkdir(parents=True, exist_ok=True)
        
        plan_path = context_dir / "planning.md"
        self.log(f"Saving plan to: {plan_path}")
        
        try:
            with open(plan_path, "w") as f:
                f.write(f"# Implementation Plan\n\n")
                
                if "error" in workflow:
                    f.write("## ⚠️ Planning Error\n\n")
                    f.write(f"**Error**: {workflow['error']}\n\n")
                    f.write("### Raw LLM Output\n\n")
                    f.write("```\n")
                    f.write(workflow.get("raw_content", ""))
                    f.write("\n```\n")
                else:
                    f.write(f"## Architecture\n")
                    arch = workflow.get("architecture", {})
                    for component, files in arch.items():
                        f.write(f"### {component}\n")
                        for file in files:
                            f.write(f"- {file}\n")
                    
                    f.write(f"\n## Tasks\n")
                    for task in workflow.get("tasks", []):
                        f.write(f"- [{task.get('phase')}] {task.get('description')} (Agent: {task.get('agent')})\n")
            self.log(f"Plan saved successfully")
        except Exception as e:
            self.log(f"Failed to save plan: {e}")

    async def identify_search_queries(self, user_prompt: str, existing_files: List[str]) -> List[str]:
        """Identify relevant search queries using LLM."""
        system_prompt = SystemMessage(content="""You are an intelligent code navigator. 
        Given a user request and a list of existing files, identify up to 3 specific keywords or exact filenames to search for in the codebase that are most relevant to the request.
        Return ONLY a JSON list of strings, e.g. ["keyword1", "filename.py", "function_name"]""")
        
        file_list = ", ".join(existing_files) if existing_files else "No files yet"
        user_message = HumanMessage(content=f"Request: {user_prompt}\nExisting Files: {file_list}")
        
        try:
            response = await self.retry_operation(self.model.ainvoke, [system_prompt, user_message])
            content = response.content.replace("`", "").strip()
            # Extract list from potential JSON/text
            match = re.search(r"\[.*\]", content, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            return []
        except Exception as e:
            self.log(f"Failed to generate search queries: {e}")
            return []
