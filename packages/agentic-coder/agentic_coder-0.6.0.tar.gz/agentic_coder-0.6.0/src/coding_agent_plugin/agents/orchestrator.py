"""Orchestration agent for routing tasks to other agents."""

from typing import Dict, Any
from acp.client import InProcessACPClient
from coding_agent_plugin.managers import ProjectManager
# Agents are loaded dynamically


from .base_agent import BaseAgent

class OrchestratorAgent(BaseAgent):
    """Agent responsible for orchestrating tasks to other agents using IBM ACP SDK."""

    def __init__(self) -> None:
        super().__init__(name="orchestrator")
        # Initialize all agents
        self.agents = {}
        self._load_agents()

    def _load_agents(self) -> None:
        """Dynamically load agents from the agents package."""
        import pkgutil
        import importlib
        import inspect
        from .base_agent import BaseAgent
        import coding_agent_plugin.agents as agents_pkg

        
        package_path = agents_pkg.__path__
        prefix = agents_pkg.__name__ + "."

        for _, name, _ in pkgutil.iter_modules(package_path, prefix):
            try:
                module = importlib.import_module(name)
                for _, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseAgent) and 
                        obj is not BaseAgent):
                        
                        agent_name = getattr(obj, "name", None) or name.split(".")[-1].replace("_agent", "")
                        simple_name = name.split(".")[-1]
                        
                        # Special handling for known agents to preserve current functionality
                        if simple_name == "planning":
                            self.agents["planning"] = obj(name="planning")
                        elif simple_name == "coding":
                            self.agents["coding"] = obj(name="coding")
                        elif simple_name == "task":
                            self.agents["task"] = obj(name="task")
                        elif simple_name == "error":
                            self.agents["error"] = obj(name="error")
                        elif simple_name == "execution":
                            self.agents["execution"] = obj(name="execution")
                        else:
                            # Auto-register new agents
                            try:
                                instance = obj(name=agent_name)
                                self.agents[agent_name] = instance
                                self.log(f"🔌 Loaded plugin agent: {agent_name} ({obj.__name__})")
                            except Exception as e:
                                self.log(f"⚠️ Failed to load agent {name}: {e}")
            except Exception as e:
                self.log(f"⚠️ Failed to import module {name}: {e}")
        
        # Initialize ACP client for in-process communication
        self.acp_client = InProcessACPClient(self.agents)

    async def send_to_agent(self, agent_name: str, payload: dict) -> dict:
        """Send a message to an agent using IBM ACP SDK client."""
        return await self.acp_client.send_to_agent(agent_name, payload)

    async def execute(self, task: dict[str, Any]) -> dict[str, Any]:
        """
        Execute the orchestration task.
        
        Args:
            task: Task dictionary containing 'user_message' and 'project_id' usually.
        """
        self.logger.info("Orchestrator starting execution...")
        
        # Initialize Analytics (ensure tables)
        from coding_agent_plugin.services.analytics import analytics
        await analytics.ensure_tables()
        
        project_id = task.get("project_id", "adhoc")
        user_prompt = task.get("user_prompt") or task.get("user_message")
        
        # Audit Log: Start
        start_details = {
            "task": task,
            "session_config": {
                "model": task.get("model") or "default",
                "provider": task.get("provider") or "default"
            }
        }
        await analytics.log_action(project_id, "ORCHESTRATOR_START", start_details)

        # Special Modes
        mode = task.get("mode")
        if mode == "analysis" or mode == "documentation":
             from .documentation import DocumentationAgent
             doc_agent = DocumentationAgent()
             return await doc_agent.execute(task)

        if mode == "autonomous":
            return await self.run_project(user_prompt, project_id)

        # Alias mapping (kept for other modes that might use it)
        if mode == "analysis": # This case is now handled above, but keeping for robustness
            mode = "documentation"
            
        if mode not in self.agents:
            raise ValueError(f"Unsupported mode: {mode}")

        agent = self.agents[mode]
        task = {
            "user_prompt": user_prompt,
            "project_id": project_id
        }
        return await agent.execute(task)

    async def run_project(self, user_prompt: str, project_id: str) -> Dict[str, Any]:
        """Run the full autonomous project creation loop."""
        self.log(f"🚀 Starting autonomous project: {project_id}")
        
        # 0. Ensure Project Exists
        pm = ProjectManager()
        if not pm.get_project(project_id):
            self.log(f"✨ Creating new project '{project_id}'...")
            try:
                pm.create_project(project_id, description=user_prompt[:200])
            except Exception as e:
                self.log(f"⚠️ Failed to create project: {e}")
                
        # 1. Planning Phase
        self.log("📋 Phase 1: Planning")
        planning_task = {
            "user_prompt": user_prompt,
            "project_id": project_id
        }
        plan_result = await self.send_to_agent("planning", planning_task)
        
        workflow = plan_result.get("workflow", {})
        tasks = workflow.get("tasks", [])
        
        if not tasks:
            self.log("⚠️ No tasks generated in plan.")
            return {"status": "failed", "error": "No tasks in plan"}

        # Initialize tasks.md via TaskAgent
        await self.agents["task"].execute({
            "project_id": project_id,
            "action": "init_tasks",
            "tasks": tasks
        })

        self.log(f"⚙️ Phase 2: Execution ({len(tasks)} tasks)")
        results = []
        MAX_RETRIES = 2
        
        pm = ProjectManager()
        project = pm.get_project(project_id)
        if not project:
            raise ValueError(f"Project '{project_id}' not found")
            
        project_path = project["storage_path"]
        
        for i, task in enumerate(tasks, 1):
            description = task.get("description")
            agent_type = task.get("agent", "coding")
            
            self.log(f"👉 Task {i}: {description} (Agent: {agent_type})")
            
            # Mark as in-progress
            await self.agents["task"].execute({
                "project_id": project_id,
                "action": "update_status",
                "task_description": description,
                "status": "in_progress"
            })
            
            task_input = {
                "user_prompt": description,
                "project_id": project_id,
                "project_path": project_path,
                **task.get("details", {})
            }
            
            retry_count = 0
            while retry_count <= MAX_RETRIES:
                try:
                    result = None
                    if agent_type == "coding":
                        result = await self.send_to_agent("coding", task_input)
                    elif agent_type == "execution":
                        result = await self.send_to_agent("execution", task_input)
                    elif agent_type == "task":
                        # TaskAgent is execution log
                        result = {"status": "completed", "message": "Task tracked"}
                    else:
                        self.log(f"⚠️ Unknown agent type: {agent_type}")
                        result = {"status": "skipped"}
                    
                    results.append({"task": description, "status": "completed", "result": result})
                    self.log(f"✅ Success")
                    
                    # Mark as completed
                    await self.agents["task"].execute({
                        "project_id": project_id,
                        "action": "update_status",
                        "task_description": description,
                        "status": "completed"
                    })
                    break
                    
                except Exception as e:
                    retry_count += 1
                    self.log(f"❌ Error: {e} (attempt {retry_count})")
                    
                    # Trigger ErrorAgent if appropriate
                    if agent_type != "error" and retry_count < MAX_RETRIES:
                        self.log(f"🚑 Attempting recovery with ErrorAgent...")
                        
                        try:
                            error_agent = self.agents["error"]
                            error_task_input = {
                                "error": str(e),
                                "file_path": task_input.get("file_path"), # Might be None
                                "project_id": project_id,
                                "project_path": project_path,
                                "user_prompt": str(e) # Pass error as prompt for fixes
                            }
                            
                            await error_agent.execute(error_task_input)
                            self.log(f"🔧 Error fixed, retrying task...")
                            
                        except Exception as error_fix_exception:
                            self.log(f"⚠️ Error recovery failed: {error_fix_exception}")
                            
                    else:
                        # No more retries or this was the ErrorAgent itself
                        results.append({"task": description, "status": "failed", "error": str(e), "retries": retry_count})
                        self.log(f"💀 Task failed after {retry_count} attempts")
                        break
                    
        # Final result
        result_payload = {"status": "completed", "results": results}
        
        # Audit Log: Complete
        from coding_agent_plugin.services.analytics import analytics
        await analytics.log_action(project_id, "ORCHESTRATOR_COMPLETE", {
            "status": "success",
            "task_count": len(results),
            "summary": f"Completed {len(results)} tasks."
        })
        
        return result_payload
