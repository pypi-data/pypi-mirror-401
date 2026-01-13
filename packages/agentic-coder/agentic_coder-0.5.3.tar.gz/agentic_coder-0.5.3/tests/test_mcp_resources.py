
import asyncio
import os
import shutil
from pathlib import Path
from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.agents.base_agent import BaseAgent

# Mock Agent to access get_project_context
class MockAgent(BaseAgent):
    async def execute(self, task): pass

async def test_mcp_resources():
    print("🚀 Testing Internal MCP Resources...")
    
    # Setup: Create a test project
    pm = ProjectManager()
    project_name = "test_mcp_project"
    
    # Cleanup if exists
    existing = pm.get_project(project_name)
    if existing:
        pm.delete_project(existing['id'])
        
    print(f"Creating project: {project_name}")
    project = pm.create_project(project_name, "MCP Test Project")
    project_id = project['id']
    storage_path = Path(project['storage_path'])
    
    # Create some files
    (storage_path / "hello.py").write_text('print("Hello MCP World")\n# TODO: Fix this', encoding="utf-8")
    (storage_path / "README.md").write_text('# Test Project\nThis is a test.', encoding="utf-8")
    
    agent = MockAgent("test_agent")
    
    # Test 1: Read Resource (project://...)
    print("\n[Test 1] Reading Resource: project://.../hello.py")
    content = await agent.get_project_context(project_id, file_path="hello.py")
    print(f"Content:\n{content}")
    assert 'print("Hello MCP World")' in content
    print("✅ Resource Read Success")
    
    # Test 2: Search Tool
    print("\n[Test 2] Searching Code: 'TODO'")
    search_results = await agent.get_project_context(project_id, query="TODO")
    print(f"Results:\n{search_results}")
    assert "hello.py" in search_results and "TODO: Fix this" in search_results
    print("✅ Search Tool Success")
    
    # Cleanup
    pm.delete_project(project_id)
    print("\n✨ All MCP tests passed!")

if __name__ == "__main__":
    asyncio.run(test_mcp_resources())
