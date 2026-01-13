"""FastAPI Server implementation for exposing agents.

This module sets up the HTTP server that allows external users/systems to
connect to and invoke the agents via a standard REST API.
"""

from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from contextlib import asynccontextmanager

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

# Global orchestrator instance
orchestrator: Optional[OrchestratorAgent] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agents on startup."""
    global orchestrator
    print("🚀 Initializing Agent Orchestrator...")
    orchestrator = OrchestratorAgent()
    print(f"✅ Loaded Agents: {list(orchestrator.agents.keys())}")
    yield
    print("👋 Shutting down Agent Server")

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Coder API",
    description="Public API to interact with the Agentic Coder agents.",
    version="0.5.2",
    lifespan=lifespan
)

class AgentRequest(BaseModel):
    """Request model for agent invocation."""
    user_prompt: str
    project_id: str
    details: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    """Response model from agent."""
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "agentic-coder",
        "agents": list(orchestrator.agents.keys()) if orchestrator else []
    }

@app.post("/agent/{agent_name}")
async def invoke_agent(agent_name: str, request: AgentRequest):
    """
    Invoke a specific agent by name.
    
    Args:
        agent_name: Name of the agent (e.g., 'coding', 'planning')
        request: Input payload containing prompt and context
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
        
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' not found")

    try:
        # Construct payload for the agent
        payload = {
            "user_prompt": request.user_prompt,
            "project_id": request.project_id,
            **request.details
        }
        
        # Route via orchestrator
        # We use the internal send_to_agent which eventually calls agent.execute
        # For 'autonomous' executions, one might call a specific endpoint, 
        # but here we expose direct agent access as requested.
        
        result = await orchestrator.send_to_agent(agent_name, payload)
        
        return {
            "status": "success", 
            "result": result
        }
        
    except Exception as e:
        # Log the error (FastAPI will also log it)
        print(f"❌ Error invoking agent {agent_name}: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

@app.post("/autonomous")
async def run_autonomous(request: AgentRequest):
    """Run the full autonomous project creation loop."""
    if not orchestrator:
         raise HTTPException(status_code=503, detail="Orchestrator not initialized")

    try:
        result = await orchestrator.run_project(
            user_prompt=request.user_prompt,
            project_id=request.project_id
        )
        return {"status": "completed", "result": result}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the server using uvicorn."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)
