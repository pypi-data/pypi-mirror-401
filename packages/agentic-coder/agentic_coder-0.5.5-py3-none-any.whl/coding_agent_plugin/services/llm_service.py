"""Service for handling LLM calls."""

from httpx._models import Response
from typing import Any
import httpx
from ..core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


class LLMService:
    """Service for handling LLM calls."""

    url: str
    model: str
    api_key: str

    def __init__(self) -> None:
        if not LLM_BASE_URL:
            raise ValueError("LLM_BASE_URL not configured")
        if not LLM_API_KEY:
            raise ValueError("LLM_API_KEY not configured")
        if not LLM_MODEL:
            raise ValueError("LLM_MODEL not configured")
        self.url = LLM_BASE_URL
        self.model = LLM_MODEL
        self.api_key = LLM_API_KEY

    async def call_llm(self, prompt: str, project_id: str = "unknown") -> dict[str, Any]:
        """Call the LLM with the given prompt."""
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data: dict[str, str] = {
            "model": self.model,
            "prompt": prompt,
        }
        
        # Calculate input tokens (rough estimate or use tiktoken if available)
        # For now, approximate 1 word = 1.3 tokens or just len(prompt)/4
        input_tokens = len(prompt) // 4
        
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(self.url, headers=headers, json=data)
            _ = response.raise_for_status()
            result = response.json()
            
            # Example token count (adjust based on your LLM response format)
            usage = result.get("usage", {})
            params = {
                "input_tokens": usage.get("prompt_tokens", input_tokens),
                "output_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
            
            # Record Analytics (Cost calculated automatically)
            from .analytics import analytics
            await analytics.track_token_usage(
                project_id=project_id,
                model=self.model,
                input_tokens=params["input_tokens"],
                output_tokens=params["output_tokens"],
                total_tokens=params["total_tokens"]
            )
            
            return {
                "response": result,
                "tokens_used": params["total_tokens"],
            }

    async def get_response(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        """Helper to get text response from LLM."""
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]
        
        headers: dict[str, str] = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"} if json_mode else None
        }
        
        async with httpx.AsyncClient() as client:
            response: Response = await client.post(self.url + "/chat/completions", headers=headers, json=data)
            _ = response.raise_for_status()
            result = response.json()
            
            # Simple OpenAI usage tracking (optional, kept simple here to avoid recursive analytics calls for intent checks?)
            # Actually call_llm handles non-chat?
            # Adjust to match the existing pattern or use call_llm if possible?
            # call_llm seems to use a custom payload "prompt": prompt.
            # If the user is using OpenAI, "prompt" is for completions, "messages" for chat.
            # Assuming 'call_llm' was basic.
            
            content = result["choices"][0]["message"]["content"]
            return content

llm_service = LLMService()
