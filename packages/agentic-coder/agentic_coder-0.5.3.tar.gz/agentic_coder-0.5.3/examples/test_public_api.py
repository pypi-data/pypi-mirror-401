
import os
import sys
import time

# Ensure src is in path
sys.path.append(os.path.abspath("src"))

try:
    from fastapi.testclient import TestClient
    from coding_agent_plugin.acp.server import app
except ImportError:
    print("❌ Critical dependencies missing. Please install fastapi and httpx.")
    sys.exit(1)

def test_public_api():
    print("🧪 Testing Public API (Agent Interface)...\n")
    
    # TestClient context triggers the lifespan (startup/shutdown) events
    print("1️⃣  Starting Test Client (initializing agents)...")
    with TestClient(app) as client:
        
        # Test 1: Health Check
        print("\n2️⃣  Testing Health Endpoint [GET /]...")
        response = client.get("/")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {response.status_code}")
            print(f"   ✅ Service: {data.get('service')}")
            print(f"   ✅ Active Agents: {data.get('agents')}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")
            
        # Test 2: Invoke Agent
        print("\n3️⃣  Testing Agent Invocation [POST /agent/task]...")
        payload = {
            "user_prompt": "Are you online?",
            "project_id": "api_test_project",
            "details": {"action": "log_check"} # Simple action that doesn't modify files
        }
        
        response = client.post("/agent/task", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Status: {result.get('status')}")
            print(f"   ✅ Response: {result.get('result')}")
        else:
            print(f"   ❌ Failed: {response.status_code} - {response.text}")

        # Test 3: Error Handling (Missing Agent)
        print("\n4️⃣  Testing Error Handling [POST /agent/missing_agent]...")
        response = client.post("/agent/missing_agent", json=payload)
        
        if response.status_code == 404:
            print(f"   ✅ Correctly handled 404: {response.json().get('detail')}")
        else:
             print(f"   ❌ Unexpected response: {response.status_code}")

if __name__ == "__main__":
    test_public_api()
