"""ACP Client for invoking agents through the ACP protocol.

This module provides a client for communicating with ACP-compliant agents.
"""

from typing import Any, Dict


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
        try:
            from acp_sdk.client import Client
        except ImportError:
            raise ImportError("acp-sdk is required for ACPClient. Please install it.")
        self.client = Client(base_url=base_url)
    
    async def send_to_agent(self, agent_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to an ACP agent.
        
        Args:
            agent_name: Name of the agent to invoke
            payload: Request payload dictionary
            
        Returns:
            Agent's response as a dictionary
        """
        from acp_sdk.models import Message
        from acp_sdk.models.models import MessagePart
        
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
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found")
            
        # Analytics Tracking
        try:
             from coding_agent_plugin.services.analytics import analytics
             project_id = payload.get("project_id", "unknown")
             
             # Extract relevant details for logging
             log_details = {
                 "agent": agent_name
             }
             for key in ["user_prompt", "command", "file_path", "action", "task_description"]:
                 if key in payload:
                     log_details[key] = payload[key]

             # Dynamic Action Name
             agent_key = agent_name.upper().replace(" ", "_")
             start_action = f"{agent_key}_START"
             
             # Log Start
             await analytics.log_action(project_id, start_action, log_details)
        except:
             pass 

        # Direct invocation (no ACP overhead for in-process)
        try:
            result = await agent.execute(payload)
            
            # Log Success
            try:
                complete_action = f"{agent_key}_COMPLETE"
                result_details = {
                    "status": result.get("status", "unknown")
                }
                # Capture created/modified file info
                if "file_path" in result:
                     result_details["file_path"] = result["file_path"]
                if "error" in result:
                     result_details["error"] = result["error"]
                     
                await analytics.log_action(project_id, complete_action, result_details)
            except: 
                pass
                
            return result
            
        except Exception as e:
            # Log Failure
            try:
                failed_action = f"{agent_key}_FAILED"
                await analytics.log_action(project_id, failed_action, {
                    "error": str(e)
                })
            except:
                pass
            raise e
