import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load env variables (API keys)
load_dotenv()

from coding_agent_plugin.agents.documentation import DocumentationAgent

# 1. Create a dummy file to refine
TEST_FILE = Path("examples/dummy_doc.md")
TEST_FILE.write_text("# Old Title\n\nThis is old content.", encoding="utf-8")

async def test_refinement():
    print(f"Original Content:\n{TEST_FILE.read_text()}\n---")
    
    # 2. Instantiate the Agent
    agent = DocumentationAgent()
    
    # 3. Define the Refinement Task
    # This payload matches what the CLI sends internally
    task = {
        "project_id": "programmatic_test",
        "refine_path": str(os.path.abspath(TEST_FILE)),
        "instruction": "Change the title to 'New Programmatic Title' and add a bullet point about Python API."
    }
    
    print(f"🚀 Sending refinement request: '{task['instruction']}'...")
    
    # 4. Execute
    result = await agent.execute(task)
    
    if result.get("status") == "completed":
        print("\n✅ Refinement Successful!")
        print(f"New Content:\n{TEST_FILE.read_text()}")
    else:
        print(f"\n❌ Error: {result.get('error')}")

if __name__ == "__main__":
    asyncio.run(test_refinement())
