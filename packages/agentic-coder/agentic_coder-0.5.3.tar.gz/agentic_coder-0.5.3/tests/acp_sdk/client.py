from typing import Dict, Any
import httpx
from .models import Message

class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def run_sync(self, agent_name: str, input: Dict[str, Any]) -> Dict[str, Any]:
        # Serialize input
        # input is {"messages": [Message...]}
        json_input = {"messages": []}
        for m in input["messages"]:
            parts = [{"content": p.content} for p in m.parts]
            json_input["messages"].append({"parts": parts})

        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/run/{agent_name}", json=json_input)
            response.raise_for_status()
            return response.json()
