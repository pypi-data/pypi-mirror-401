"""ACP Client for invoking agents through the ACP protocol.

This module provides a client for communicating with ACP-compliant agents.
"""

from typing import Any, Dict
from acp_sdk.client import Client
from acp_sdk.models import Message
from acp_sdk.models.models import MessagePart


class ACPClient:
    """Client for communicating with ACP-compliant agents.
    
    This client handles:
    - Converting internal payload to ACP Message format
    - Invoking agents via ACP protocol
    - Converting ACP responses back to internal format
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the ACP client.
        
        Args:
            base_url: Base URL of the ACP server
        """
        self.client = Client(base_url=base_url)
    
    async def send_to_agent(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to an ACP agent.
        
        Args:
            agent_name: Name of the agent to invoke
            payload: Request payload dictionary
            
        Returns:
            Agent's response as a dictionary
        """
        # Convert payload to ACP Message format
        content = str(payload)
        messages = [Message(parts=[MessagePart(content=content)])]
        
        # Invoke the agent via ACP
        response = await self.client.run_sync(
            agent_name=agent_name,
            input={"messages": messages}
        )
        
        # Extract the response content
        # This is a simplified version - you may need to parse the response more carefully
        return {"result": response}


class InProcessACPClient:
    """In-process ACP client for direct agent invocation.
    
    This is used when agents are in the same process (not over HTTP).
    """
    
    def __init__(self, agents: Dict[str, Any]):
        """Initialize with a mapping of agent instances.
        
        Args:
            agents: Dictionary mapping agent names to agent instances
        """
        self.agents = agents
    
    async def send_to_agent(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to an agent directly (in-process).
        
        Args:
            agent_name: Name of the agent to invoke
            payload: Request payload dictionary
            
        Returns:
            Agent's response as a dictionary
        """
        agent = self.agents.get(agent_name)
        # Analytics Tracking - EXPOSED ERRORS
        from coding_agent_plugin.services.analytics import analytics
        project_id = payload.get("project_id", "unknown")
        
        # Log Start
        await analytics.log_action(project_id, "AGENT_EXECUTION_START", {
            "agent": agent_name,
            "payload_keys": list(payload.keys())
        })

        # Direct invocation (no ACP overhead for in-process)
        try:
            result = await agent.execute(payload)
            
            # Log Success
            await analytics.log_action(project_id, "AGENT_EXECUTION_COMPLETE", {
                "agent": agent_name,
                "status": result.get("status", "unknown")
            })
                
            return result
            
        except Exception as e:
            # Log Failure
            await analytics.log_action(project_id, "AGENT_EXECUTION_FAILED", {
                "agent": agent_name,
                "error": str(e)
            })
            raise e
