import asyncio
import os
import shutil
from unittest.mock import MagicMock, patch
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def test_orchestrator():
    project_id = "test_project_123"
    
    # Mock ChatOpenAI
    # Mock ChatOpenAI globally
    with patch("langchain_openai.ChatOpenAI") as MockLLM:
        
        # Setup mocks for each agent (Planning, Coding, Error)
        mock_planning_llm = MagicMock()
        mock_coding_llm = MagicMock()
        mock_error_llm = MagicMock()
        
        # Side effect order: Planning, Coding, Error
        MockLLM.side_effect = [mock_planning_llm, mock_coding_llm, mock_error_llm]
        
        # Setup return values
        mock_planning_llm.stream.return_value = [{"content": "Mock plan"}]
        
        future_coding = asyncio.Future()
        future_coding.set_result(MagicMock(content="print('Hello World')"))
        mock_coding_llm.ainvoke.return_value = future_coding
        
        future_error = asyncio.Future()
        future_error.set_result(MagicMock(content="print('Hello World Fixed')"))
        mock_error_llm.ainvoke.return_value = future_error
            
        orchestrator = OrchestratorAgent()

        # Clean up previous run
        if os.path.exists(f"projects/{project_id}"):
            shutil.rmtree(f"projects/{project_id}")

        from coding_agent_plugin.managers import ProjectManager
        pm = ProjectManager()
        if pm.get_project(project_id):
            pm.delete_project(project_id)
        if pm.get_project(project_id):
            pm.delete_project(project_id)
        project = pm.create_project(project_id, "Test Project")
        project_dir = project["storage_path"]

        print("Testing Planning Agent...")
        # We need to mock the plan method return value because we mocked the internal agent
        # Actually, let's just mock the plan method of PlanningAgent to simplify
        with patch.object(orchestrator.agents["planning"], "plan", return_value=[{"task": "test", "agent": "coding"}]) as mock_plan:
            await orchestrator.execute("planning", "Create a simple calculator", project_id)
            if os.path.exists(f"{project_dir}/planning.md"):
                print("Planning Agent: SUCCESS")
            else:
                print("Planning Agent: FAILED")

        print("Testing Coding Agent...")
        await orchestrator.execute("coding", "Write a python function to add two numbers", project_id)
        if os.path.exists(f"{project_dir}/generated_code.py"):
            print("Coding Agent: SUCCESS")
        else:
            print("Coding Agent: FAILED")

        print("Testing Task Agent...")
        await orchestrator.execute("task", "Implement addition function", project_id)
        if os.path.exists(f"{project_dir}/tasks.md"):
            print("Task Agent: SUCCESS")
        else:
            print("Task Agent: FAILED")
            
        print("Testing Error Agent...")
        # Introduce an error first (manually for test)
        with open(f"{project_dir}/generated_code.py", "w") as f:
            f.write("def add(a, b): return a + b + 'error'")
            
        await orchestrator.execute("error", "Fix syntax error", project_id)


        # Since we mocked the return value to "print('Hello World Fixed')", checking for that
        with open(f"{project_dir}/generated_code.py", "r") as f:
            content = f.read()
            if "Fixed" in content:
                    print("Error Agent: SUCCESS")
            else:
                    print(f"Error Agent: FAILED. Content: {content}")

        print("Testing Execution Agent...")
        # Write valid code for execution test
        with open(f"{project_dir}/generated_code.py", "w") as f:
            f.write("print('Hello from Execution Agent')")
            
        await orchestrator.execute("execution", "Run the code", project_id)
        if os.path.exists(f"{project_dir}/execution.md"):
            print("Execution Agent: SUCCESS")
        else:
            print("Execution Agent: FAILED")

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
