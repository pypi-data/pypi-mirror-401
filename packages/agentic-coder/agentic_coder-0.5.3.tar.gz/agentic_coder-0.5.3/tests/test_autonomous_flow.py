import asyncio
import os
import shutil
from unittest.mock import MagicMock, patch
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def test_autonomous_flow():
    project_id = "auto_project_456"
    
    # Mock ChatOpenAI globally since agents now import it inside get_llm
    with patch("langchain_openai.ChatOpenAI") as MockLLM:
        
        # Setup mocks for each agent
        mock_planning_llm = MagicMock()
        mock_coding_llm = MagicMock()
        mock_error_llm = MagicMock()
        
        # Orchestrator inits agents in order: Planning, Coding, Task, Error, Execution
        # Only Planning, Coding, and Error use LLM in this flow
        # We need to ensure side_effect returns them in correct order of instantiation
        MockLLM.side_effect = [mock_planning_llm, mock_coding_llm, mock_error_llm]
        
        # Mock the LLM response for PlanningAgent to return JSON string
        import json
        mock_plan = {
            "architecture": {
                "backend": ["main.py"]
            },
            "tasks": [
                {
                    "id": 1,
                    "phase": "scaffold",
                    "description": "Initialize project structure",
                    "agent": "task",
                    "details": {"action": "create_dirs", "paths": ["backend"]}
                },
                {
                    "id": 2,
                    "phase": "coding",
                    "description": "Create backend API",
                    "agent": "coding",
                    "details": {"file_path": "backend/main.py", "prompt": "Create a FastAPI app"}
                },
                {
                    "id": 3,
                    "phase": "verification",
                    "description": "Verify backend",
                    "agent": "execution",
                    "details": {"command": f"ls projects/{project_id}/backend/main.py"}
                }
            ]
        }
        
        future_planning = asyncio.Future()
        future_planning.set_result(MagicMock(content=json.dumps(mock_plan)))
        mock_planning_llm.ainvoke.return_value = future_planning
        
        future_coding = asyncio.Future()
        future_coding.set_result(MagicMock(content="print('Hello Autonomous World')"))
        mock_coding_llm.ainvoke.return_value = future_coding
        
        # Patch create_agent in planning.py
        # We don't need to patch create_agent anymore since we removed it in favor of direct LLM call
        
        orchestrator = OrchestratorAgent()

        # Clean up previous run
        from coding_agent_plugin.managers import ProjectManager
        pm = ProjectManager()
        if pm.get_project(project_id):
            pm.delete_project(project_id)
            
        # Create project in DB
        pm.create_project(project_id, "Test Project")
            
        if os.path.exists(f"projects/{project_id}"):
            shutil.rmtree(f"projects/{project_id}")

        print("Testing Autonomous Flow...")
        
        # We don't need to patch 'plan' method anymore, we are testing the real plan method with mocked LLM
        await orchestrator.execute("autonomous", "Create a simple app", project_id)
                
        # Verification
        if os.path.exists(f"projects/{project_id}/backend/main.py"):
            print("Autonomous Flow: SUCCESS - File created")
        else:
            print("Autonomous Flow: FAILED - File not created")
            
        if os.path.exists(f"projects/{project_id}/.agent_context/planning.md"):
            print("Autonomous Flow: SUCCESS - Plan saved")

if __name__ == "__main__":
    asyncio.run(test_autonomous_flow())
