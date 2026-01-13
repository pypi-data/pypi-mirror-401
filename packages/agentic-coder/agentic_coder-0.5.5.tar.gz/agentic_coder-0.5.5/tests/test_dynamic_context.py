
import asyncio
from pathlib import Path
from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.agents.planning import PlanningAgent

async def test_dynamic_context():
    print("🚀 Testing Dynamic MCP Context Retrieval...")
    
    # Setup: Create a test project with a potential "users list" bug
    pm = ProjectManager()
    project_name = "test_dynamic_context_project"
    
    existing = pm.get_project(project_name)
    if existing:
        pm.delete_project(existing['id'])
        
    project = pm.create_project(project_name, "Dynamic Context Test")
    project_id = project['id']
    storage_path = Path(project['storage_path'])
    
    # Create a file that matches the "users list" query
    (storage_path / "users_api.py").write_text("""
def get_users_list():
    # TODO: Implement this properly
    return [] # empty list for now
    
def get_user_by_id(user_data):
    pass
""", encoding="utf-8")
    
    # Initialize Planning Agent (Mocking LLM partially)
    agent = PlanningAgent("planner")
    
    # Test Prompt: "users list not coming"
    # We expect the agent to extract "users", "list" and search, finding "users_api.py"
    prompt = "users list not coming"
    print(f"\nPrompt: '{prompt}'")
    
    # We can't easily mock the full LLM call in this simple script without dependencies,
    # but we can verify the search logic by calling the extraction/search part if we exposed it,
    # OR we can just run execute() and check the logs/output if we mock the `plan` method or rely on the agent's logic.
    
    # Let's peek at the internal logic using get_project_context with the extracted keyword manually to verify the tool works
    print("Simulating agent keyword extraction: 'users', 'list'")
    kw = "users"
    
    print(f"Searching for keyword: '{kw}'")
    results = await agent.get_project_context(project_id, query=kw)
    
    print(f"Search Results:\n{results}")
    
    assert "users_api.py" in results
    assert "def get_users_list():" in results
    print("✅ Found relevant code context for vague query.")

    # Cleanup
    pm.delete_project(project_id)
    print("\n✨ Dynamic context test passed!")

if __name__ == "__main__":
    asyncio.run(test_dynamic_context())
