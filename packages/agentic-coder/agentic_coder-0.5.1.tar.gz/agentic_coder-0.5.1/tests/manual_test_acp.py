import asyncio
import sys
import os

# Add src to path so we can import the plugin
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from coding_agent_plugin.acp.client import ACPClient

async def main():
    print("🔌 Connecting to ACP Server at http://localhost:8000...")
    client = ACPClient(base_url="http://localhost:8000")
    
    print("📤 Sending request to 'planning' agent...")
    try:
        # Simple payload to test connectivity
        payload = {
            "user_prompt": "Create a simple hello world python script",
            "project_id": "test_project"
        }
        
        response = await client.send_to_agent("planning", payload)
        print("\n✅ Response received:")
        print(response)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
