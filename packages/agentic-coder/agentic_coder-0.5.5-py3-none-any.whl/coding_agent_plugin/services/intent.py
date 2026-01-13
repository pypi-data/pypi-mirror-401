import json
from typing import Dict, Any, Optional
from coding_agent_plugin.services.llm_service import llm_service

class IntentService:
    """Analyzes user prompts to determine the best execution mode."""

    @staticmethod
    async def analyze_intent(prompt: str) -> Dict[str, Any]:
        """
        Analyze prompt to determine:
        - mode: 'direct' or 'autonomous'
        - requires_new_project: bool
        - suggested_template: str | None
        """
        system_prompt = """
        You are an intelligent intent classifier for a coding assistant.
        Analyze the user's request and categorize it.
        
        Output JSON only:
        {
            "mode": "direct" | "autonomous",
            "requires_new_project": boolean,
            "suggested_template": "react-vite" | "python-fastapi" | "nextjs" | "python-basic" | null,
            "reasoning": "brief explanation"
        }
        
        Rules:
        - "direct": Simple tasks, single file creation, bug fixes, small scripts.
        - "autonomous": Complex apps, multi-file projects, "create a project", "build a website".
        - "requires_new_project": True if user asks to "start/create a new project/app". False if modifying existing or just "create a file".
        - "suggested_template": Match standard frameworks if requested (React, FastAPI, Next.js).
        """
        
        try:
            response = await llm_service.get_response(
                system_prompt=system_prompt,
                user_prompt=prompt,
                json_mode=True
            )
            return json.loads(response)
        except Exception as e:
            # Fallback
            return {
                "mode": "autonomous", # Default to safe/planned
                "requires_new_project": False,
                "suggested_template": None,
                "reasoning": f"Analysis failed: {e}"
            }
