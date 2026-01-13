
import requests
import json
import time

API_URL = "http://localhost:8000"

def test_big_project():
    print("🏗️  Testing End-to-End Project Build via ACP...")
    
    # 1. Health Checks
    try:
        resp = requests.get(f"{API_URL}/")
        print(f"   ✅ Server Online: {resp.json()}")
    except Exception as e:
        print(f"   ❌ Server connection failed: {e}")
        return

    # 2. Define Big Project
    project_id = "acp_task_manager"
    prompt = (
        "Create a Task Management API using FastAPI. "
        "Requirements: "
        "1. SQLite database with SQLAlchemy. "
        "2. Models: User (id, username, email), Task (id, title, description, user_id). "
        "3. REST Endpoints: Create/Read Users, Create/Read/Update/Delete Tasks. "
        "4. Include Pydantic schemas. "
        "5. No authentication needed for this demo, just basic CRUD."
    )
    
    payload = {
        "user_prompt": prompt,
        "project_id": project_id
    }
    
    print(f"\n🚀 Sending Request to /autonomous...")
    print(f"   Project ID: {project_id}")
    print(f"   Prompt: {prompt[:50]}...")
    
    start_time = time.time()
    
    # Large timeout because building a project takes time
    try:
        response = requests.post(f"{API_URL}/autonomous", json=payload, timeout=600)
        
        if response.status_code == 200:
            result = response.json()
            status = result.get("status")
            details = result.get("result", {})
            
            print(f"\n✅ Build Request Completed in {time.time() - start_time:.2f}s")
            print(f"   Status: {status}")
            print(f"   Keys returned: {list(details.keys())}")
            
            if status == "completed":
                print("\n🎉 SUCCESS: Project built successfully via ACP!")
            else:
                print(f"\n⚠️ Completed with status: {status}")
                
        else:
             print(f"\n❌ API Error: {response.status_code} - {response.text}")

    except requests.exceptions.Timeout:
        print("\n⏱️  Request Timed Out (Process still likely running on server)")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_big_project()
