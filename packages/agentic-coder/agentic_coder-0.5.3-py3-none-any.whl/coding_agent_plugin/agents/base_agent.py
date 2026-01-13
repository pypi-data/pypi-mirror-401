"""Base agent class for agent orchestration."""

from typing import Any, Dict
from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Base class for all agents."""

    def __init__(self, name: str, openapi_instance: Any = None):
        self.name = name
        self.openapi_instance = openapi_instance
        
        # Initialize logger
        from coding_agent_plugin.core.logging import get_logger
        self.logger = get_logger(f"agent.{name}")

    @abstractmethod
    async def execute(self, task: Any) -> Dict[str, Any]:
        """Execute the agent's task."""
        pass

    def log(self, message: str) -> None:
        """Log a message."""
        self.logger.info(f"[{self.name}] {message}", extra={"markup": True})

    async def retry_operation(self, func, *args, **kwargs):
        """Execute an operation with retry logic."""
        from coding_agent_plugin.core.config import AGENT_MAX_RETRIES, AGENT_RETRY_DELAY
        from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
        import openai
        
        # Define retry strategy
        @retry(
            stop=stop_after_attempt(AGENT_MAX_RETRIES),
            wait=wait_exponential(multiplier=AGENT_RETRY_DELAY, min=AGENT_RETRY_DELAY, max=10),
            retry=retry_if_exception_type((
                openai.RateLimitError,
                openai.APIConnectionError,
                openai.InternalServerError,
                TimeoutError
            )),
            reraise=True
        )
        async def _execute():
            return await func(*args, **kwargs)
            
        return await _execute()

    def get_llm(self):
        """Initialize and return the LLM model."""
        from langchain_openai import ChatOpenAI
        from coding_agent_plugin.core.config import LLM_MODEL, LLM_BASE_URL, LLM_API_KEY
        
        model_name = LLM_MODEL or "gpt-4o"
        
        # Set up ChatOpenAI with custom base_url and api_key
        kwargs = {"model": model_name, "temperature": 0.2}
        if LLM_API_KEY:
            kwargs["api_key"] = LLM_API_KEY
        if LLM_BASE_URL:
            kwargs["base_url"] = LLM_BASE_URL
            
        return ChatOpenAI(**kwargs)

    async def get_project_context(self, project_id: str, file_path: str = None, query: str = None) -> str:
        """
        Get project context using Internal MCP Resources.
        
        This simulates calling the MCP server to retrieve 'project://' resources or use tools.
        
        Args:
            project_id: Project ID
            file_path: Optional file path to read
            query: Optional search query
            
        Returns:
            String content/context
        """
        # In a real distributed system, this would use a proper MCP Client over stdio/HTTP.
        # For this internal implementation, we import the server functions directly 
        # to simulate the "Internal MCP" behavior requested.
        from coding_agent_plugin.mcp.server import read_project_file, search_code
        
        try:
            if file_path:
                # Resource: project://{id}/{path}
                return read_project_file(project_id, file_path)
            elif query:
                # Tool: search_code
                results = search_code(project_id, query)
                return "\n".join(results) if results else "No matches found."
            else:
                return "No context requested"
        except Exception as e:
            return f"Error retrieving context for {project_id}: {e}"
