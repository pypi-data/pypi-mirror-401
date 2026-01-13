"""Error agent for fixing code errors."""

import os
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from coding_agent_plugin.services.prompt_service import PromptService


class ErrorAgent(BaseAgent):
    """Agent responsible for identifying and fixing errors in code."""

    def __init__(self, name: str, openapi_instance: Any = None):
        super().__init__(name, openapi_instance)
        self.model = self.get_llm()

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the error fixing task."""
        project_id = task.get("project_id")
        error_details = task.get("user_prompt") # Assuming user prompt contains error details
        file_path = task.get("file_path") # Optional: specific file to fix
        
        if not project_id:
            raise ValueError("Missing project_id")

        self.log(f"Fixing errors for project: {project_id}")
        
        from coding_agent_plugin.managers import ProjectManager
        pm = ProjectManager()
        project = pm.get_project(project_id)
        if not project:
             raise ValueError(f"Project '{project_id}' not found")
             
        project_path = project["storage_path"]
        
        if not file_path:
             file_path = "generated_code.py"
        
        # 1. Read file using MCP Context
        code_content = await self.get_project_context(project_id, file_path=file_path)
        if code_content.startswith("Error") or "File not found" in code_content:
             return {"status": "error", "message": f"Could not read file {file_path}: {code_content}"}
            
        # 2. Fix code
        fixed_code = await self.fix_code(code_content, error_details)
        
        # 3. Save file (ProjectManager/FS)
        full_path = os.path.join(project_path, file_path)
        with open(full_path, "w") as f:
            f.write(fixed_code)
            
        return {"file_path": file_path, "status": "fixed"}

    async def fix_code(self, code: str, error: str) -> str:
        """Fix code using LLM."""
        messages = [
            SystemMessage(content=PromptService.get_error_fixing_system_prompt()),
            HumanMessage(content=f"Code:\n{code}\n\nError:\n{error}")
        ]
        response = await self.model.ainvoke(messages)
        return response.content
