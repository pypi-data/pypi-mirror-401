#!/usr/bin/env python3
"""Start the Public Agent API Server.

This script launches the FastAPI server using Uvicorn, making the agents
accessible via HTTP.

Usage:
    python -m coding_agent_plugin.acp.start_server
"""

import uvicorn
import os
from coding_agent_plugin.acp.server import app

def main():
    """Start the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Public Agent API on http://{host}:{port}")
    print(f"📖 Docs available at http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
