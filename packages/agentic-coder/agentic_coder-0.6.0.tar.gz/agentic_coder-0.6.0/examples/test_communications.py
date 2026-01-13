
import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.path.abspath("src"))

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.managers import ProjectManager

async def test_communications():
    print("🧪 Testing Agent Communications & Protocols...\n")

    # 1. Initialize Orchestrator (loads agents dynamically)
    print("1️⃣  Initializing Orchestrator (Dynamic Loading)...")
    orchestrator = OrchestratorAgent()
    print("   ✅ Orchestrator loaded with agents: ", list(orchestrator.agents.keys()))

    # 2. Test In-Process ACP Routing
    print("\n2️⃣  Testing In-Process ACP Routing...")
    try:
        # We send a "status update" request to the TaskAgent via the ACP Client
        # This proves the Orchestrator -> Client -> Agent -> Execute loop works
        payload = {
            "project_id": "test_verification_project",
            "action": "log_check",
            "user_prompt": "Verifying ACP routing"
        }
        
        # Using the internal client explicitly
        result = await orchestrator.acp_client.send_to_agent("task", payload)
        print(f"   ✅ ACP Message routed successfully. Response: {result}")
    except Exception as e:
        print(f"   ❌ ACP Routing Failed: {e}")

    # 3. Test Internal MCP Resources
    print("\n3️⃣  Testing Internal MCP Resource Access...")
    try:
        pm = ProjectManager()
        project_id = "test_mcp_project"
        
        # Create project properly using PM
        try:
            # Check if exists first to avoid error on rerun
            existing = pm.get_project(project_id)
            if existing:
                project_path = existing["storage_path"]
                print(f"   ℹ️  Using existing test project at {project_path}")
            else:
                project_data = pm.create_project(project_id, "Test Project for verification")
                project_path = project_data["storage_path"]
                print(f"   ℹ️  Created test project at {project_path}")
        except Exception as e:
            # Fallback if create failed (e.g. race condition)
            print(f"   ⚠️ Project init warning: {e}")
            existing = pm.get_project(project_id)
            project_path = existing["storage_path"]

        # Write test file to the REAL storage path
        test_file = "mcp_test.txt"
        with open(os.path.join(project_path, test_file), "w") as f:
            f.write("MCP Protocol Verified!")
            
        print(f"   ℹ️  Wrote test file to {os.path.join(project_path, test_file)}")
        
        # Test 3a: Read Resource via MCP
        print("   Testing 'get_project_context' (MCP Read)...")
        content = await orchestrator.agents["coding"].get_project_context(project_id, file_path=test_file)
        
        if "MCP Protocol Verified!" in content:
            print(f"   ✅ MCP Read Resource successful. Content: '{content}'")
        else:
            print(f"   ❌ MCP Read failed. Got: '{content}'")
            
        # Test 3b: Search via MCP (RAG capability)
        print("   Testing 'get_project_context' (MCP Search)...")
        search_results = await orchestrator.agents["coding"].get_project_context(project_id, query="Protocol")
        
        if "mcp_test.txt" in search_results and "Verified" in search_results:
             print(f"   ✅ MCP Search successful. Results:\n{search_results}")
        else:
             print(f"   ❌ MCP Search failed. Got: '{search_results}'")

    except Exception as e:
        print(f"   ❌ MCP Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_communications())
