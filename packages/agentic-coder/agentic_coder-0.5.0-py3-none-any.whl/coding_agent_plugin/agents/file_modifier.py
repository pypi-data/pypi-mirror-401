"""File modification agent for targeted code changes."""

import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent


class FileModifierAgent(BaseAgent):
    """Agent responsible for making targeted modifications to existing files."""
    
    def __init__(self, name: str, openapi_instance: Any = None):
        super().__init__(name, openapi_instance)
        self.model = self.get_llm()
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute file modification task.
        
        Args:
            task: Contains:
                - instruction: What to change
                - file_path: Path to file to modify
                - project_id: Project identifier
                - existing_content: Current file content
                
        Returns:
            Dict with modified content and change description
        """
        instruction = task.get("instruction")
        file_path = task.get("file_path")
        project_id = task.get("project_id")
        existing_content = task.get("existing_content", "")
        
        if not instruction or not file_path:
            raise ValueError("Missing instruction or file_path")
        
        self.log(f"Modifying {file_path}: {instruction}")
        
        # Generate modified content
        modified_content = await self.modify_file(instruction, existing_content, file_path)
        
        # Save modified file
        # Save modified file
        from coding_agent_plugin.managers import ProjectManager
        pm = ProjectManager()
        project = pm.get_project(project_id)
        if not project:
            raise ValueError(f"Project '{project_id}' not found")
            
        # Ensure path is relative to project root
        if file_path.startswith("/") and file_path.startswith(project["storage_path"]):
             file_path = os.path.relpath(file_path, project["storage_path"])
             
        full_path = os.path.join(project["storage_path"], file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(modified_content)
        
        return {
            "file_path": file_path,
            "modified_content": modified_content,
            "instruction": instruction
        }
    
    async def modify_file(self, instruction: str, existing_content: str, file_path: str) -> str:
        """
        Modify file content based on instruction.
        
        Args:
            instruction: What to change
            existing_content: Current file content
            file_path: Path to file (for context)
            
        Returns:
            str: Modified file content
        """
        system_content = f"""You are an expert code modification agent. Your task is to modify existing code based on user instructions.

IMPORTANT RULES:
1. Make MINIMAL changes - only modify what's necessary
2. PRESERVE all existing functionality unless explicitly asked to change it
3. Maintain the existing code style and formatting
4. Add necessary imports if you introduce new functionality
5. Return the COMPLETE modified file content
6. Do NOT include markdown formatting or explanations
7. The file is: {file_path}

Current file content:
{existing_content}

User's request:
{instruction}

Return the complete modified file."""
        
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=f"Modify the file to: {instruction}")
        ]
        
        response = await self.model.ainvoke(messages)
        modified_content = response.content
        
        # Strip markdown if present
        import re
        code_block_pattern = r"```(?:\w+)?\n?(.*?)```"
        matches = re.findall(code_block_pattern, modified_content, re.DOTALL)
        
        if matches:
            modified_content = matches[0].strip()
        
        return modified_content.strip()
