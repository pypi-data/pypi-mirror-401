from typing import Any, Callable, AsyncGenerator, Dict, List
import asyncio
import uvicorn
import threading
from fastapi import FastAPI, Request
from .models import Message, MessagePart

RunYield = Dict[str, Any]
RunYieldResume = Dict[str, Any]

class Server:
    def __init__(self):
        self.agents = {}
        self.app = FastAPI()

        @self.app.post("/run/{agent_name}")
        async def run_agent(agent_name: str, request: Request):
            data = await request.json()
            input_messages = []
            for m in data.get("messages", []):
                parts = [MessagePart(content=p["content"]) for p in m.get("parts", [])]
                input_messages.append(Message(parts=parts))
            
            if agent_name in self.agents:
                handler = self.agents[agent_name]
                # The handler is an async generator.
                # We need to run it.
                # Since we are in an async route, we can await it.
                try:
                    gen = handler(input_messages)
                    async for result in gen:
                        resp_messages = []
                        for rm in result.get("messages", []):
                            resp_parts = [{"content": p.content} for p in rm.parts]
                            resp_messages.append({"parts": resp_parts})
                        return {"messages": resp_messages}
                except Exception as e:
                    return {"error": str(e)}
            return {"error": "Agent not found"}

    def agent(self):
        def decorator(func: Callable):
            self.agents[func.__name__] = func
            return func
        return decorator

    def run(self):
        print("🚀 MOCK ACP Server starting on port 8000...")
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000)
        server = uvicorn.Server(config)
        
        # Check if we are in a loop
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            print("⚠️ Running in existing loop, starting server in thread...")
            # We can't easily run uvicorn in a thread if it needs to share the loop, but here it doesn't.
            # Uvicorn will create its own loop in the thread.
            t = threading.Thread(target=server.run)
            t.start()
            t.join()
        else:
            server.run()
