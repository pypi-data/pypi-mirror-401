from typing import Any, Dict, List
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult
from coding_agent_plugin.services.analytics import analytics
import asyncio

class SQLAnalyticsCallbackHandler(AsyncCallbackHandler):
    """Callback Handler that logs token usage to Postgres via AnalyticsService."""

    def __init__(self, project_id: str):
        self.project_id = project_id

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        try:
            # Extract usage
            if response.llm_output and "token_usage" in response.llm_output:
                usage = response.llm_output["token_usage"]
                input_tokens = usage.get("prompt_tokens", 0)
                output_tokens = usage.get("completion_tokens", 0)
                total_tokens = usage.get("total_tokens", 0)
                model_name = response.llm_output.get("model_name", "unknown")
                
                # Check for OpenAI specific structure if generic fails
                if total_tokens == 0 and "token_usage" not in response.llm_output:
                     pass
                
                # Await directly since we are in async callback
                await analytics.track_token_usage(
                    project_id=self.project_id,
                    model=model_name,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    total_tokens=total_tokens
                )
                    
        except Exception as e:
            print(f"Callback Error: {e}")

