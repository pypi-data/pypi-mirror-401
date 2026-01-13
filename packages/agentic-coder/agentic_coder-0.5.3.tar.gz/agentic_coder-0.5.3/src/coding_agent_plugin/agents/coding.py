"""Coding agent for generating code."""

import os
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from .base_agent import BaseAgent
from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.services.prompt_service import PromptService
from coding_agent_plugin.utils.token_manager import TokenManager
from coding_agent_plugin.core.config import LLM_MAX_TOKEN, LLM_MODEL


class CodingAgent(BaseAgent):
    """Agent responsible for generating code based on user prompt."""

    def __init__(self, name: str, openapi_instance: Any = None):
        super().__init__(name, openapi_instance)
        from coding_agent_plugin.core.config import LLM_MODEL, LLM_BASE_URL, LLM_API_KEY
        self.model = self.get_llm()

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the coding task."""
        
        user_prompt = task.get("user_prompt")
        project_id = task.get("project_id")
        file_path_relative = task.get("file_path") # Optional: specific file to write to
        if not file_path_relative and "details" in task:
            file_path_relative = task["details"].get("file_path")
        
        if not user_prompt or not project_id:
            raise ValueError("Missing user_prompt or project_id")

        self.log(f"Generating code for: {user_prompt}")
        
        # Get project storage path
        pm = ProjectManager()
        project = pm.get_project(project_id)
        if not project:
            raise ValueError(f"Project '{project_id}' not found")
            
        project_path = project["storage_path"]
        
        existing_content = None
        if file_path_relative:
            # Use Internal MCP to get file context
            context_response = await self.get_project_context(project_id, file_path=file_path_relative)
            if not context_response.startswith("Error"):
                existing_content = context_response
        
        
        # Get all project files for context
        project_files = pm.list_files(project_id)
        
        code_content = await self.generate_code(user_prompt, existing_content, project_files)
        
        saved_path = self.save_code(project_id, code_content, file_path_relative)
        
        return {"file_path": saved_path, "code": code_content}

    async def generate_code(self, prompt: str, existing_content: str | None = None, project_files: list[str] = None) -> str:
        """Generate code using LLM."""
        
        token_manager = TokenManager(model_name=LLM_MODEL or "gpt-4o")
        
        system_prompt_content = PromptService.get_coding_system_prompt()
        
        # Calculate tokens for mandatory parts
        system_tokens = token_manager.count_tokens(system_prompt_content)
        prompt_tokens = token_manager.count_tokens(prompt)
        
        # Reserve some buffer for response (e.g. 1000 tokens or 20% of max, whichever is smaller)
        response_buffer = min(1000, int(LLM_MAX_TOKEN * 0.2))
        available_for_context = LLM_MAX_TOKEN - system_tokens - prompt_tokens - response_buffer
        
        if available_for_context < 0:
            self.log("WARNING: Prompt + System Prompt exceeds token limit! Request might fail.")
            available_for_context = 0
            
        # Construct context parts
        project_context = ""
        if project_files:
            project_context = f"\n\nProject Structure:\n{', '.join(project_files)}\n"
            
        file_context = ""
        if existing_content:
            file_context = f"\n\nExisting content of the file:\n{existing_content}\n\nPlease update the code based on the request."
            
        # Prioritize File Content over Project Structure if we need to fit
        # Strategy: 
        # 1. Try to fit everything.
        # 2. If not, truncate Project Structure first.
        # 3. If still not enough, truncate File Content.
        
        total_context = project_context + file_context
        total_context_tokens = token_manager.count_tokens(total_context)
        
        final_context = ""
        
        if total_context_tokens <= available_for_context:
            final_context = total_context
        else:
            self.log(f"Context exceeds available space ({available_for_context}). Truncating...")
            
            # Try to fit just file content
            file_tokens = token_manager.count_tokens(file_context)
            if file_tokens <= available_for_context:
                # We have space for file content, see if we can fit some project structure
                remaining = available_for_context - file_tokens
                truncated_project = token_manager.truncate_text(project_context, remaining)
                final_context = truncated_project + file_context
            else:
                # Not enough space even for file content, drop project structure completely and truncate file content
                final_context = token_manager.truncate_text(file_context, available_for_context)
        
        full_prompt = prompt + final_context
            
        messages = [
            SystemMessage(content=system_prompt_content),
            HumanMessage(content=full_prompt)
        ]
        
        response = await self.retry_operation(self.model.ainvoke, messages)
        raw_content = response.content
        
        # Log the raw response for debugging
        self.log(f"Raw LLM response length: {len(raw_content)} chars")
        
        # Strip markdown code blocks if present
        import re
        
        # Remove markdown code blocks (```language ... ``` or ``` ... ```)
        # Find content between triple backticks
        code_block_pattern = r"```(?:\w+)?\n?(.*?)```"
        matches = re.findall(code_block_pattern, raw_content, re.DOTALL)
        
        if matches:
            # Use the first code block found
            cleaned_content = matches[0].strip()
            self.log(f"Extracted code from markdown block: {len(cleaned_content)} chars")
        else:
            # No code blocks found, use the entire content
            cleaned_content = raw_content.strip()
            
        if not cleaned_content:
            self.log("WARNING: Generated code is empty!")
            
        return cleaned_content

    def save_code(self, project_id: str, content: str, filename: str | None = None) -> str:
        """Save code to a file."""
        from coding_agent_plugin.managers import ProjectManager
        pm = ProjectManager()
        project = pm.get_project(project_id)
        
        if project:
            directory = project["storage_path"]
        else:
            # Fallback for legacy/test
            directory = os.path.abspath(f"projects/{project_id}")
            
        os.makedirs(directory, exist_ok=True)
        
        if not filename:
            filename = "generated_code.py" # Default filename
            
        # Ensure filename doesn't start with / to avoid absolute path issues
        if filename.startswith("/"):
            filename = filename[1:]
            
        file_path = os.path.join(directory, filename)
        
        # Ensure subdirectories exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        mode = "w"
        if os.path.exists(file_path):
            # "If the file already exists, it should update the file instead of creating a new one."
            # 'w' mode overwrites, which effectively updates.
            pass
            
        with open(file_path, mode) as f:
            f.write(content)
            
        return file_path
