import asyncio
import os
import shutil
import sys

# Explicitly set Analytics Envs to ensure they are picked up
os.environ["ENABLE_ANALYTICS"] = "true"
os.environ["POSTGRES_DB"] = "postgresql+asyncpg://admin:admin@localhost:5432/coding_agent"

# Ensure src is in python path
sys.path.insert(0, os.path.abspath("src"))

from dotenv import load_dotenv
load_dotenv()

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.services.analytics import analytics
from sqlalchemy import text

# Configuration
PROJECT_ID = "react_auth_test"
USER_PROMPT = """
Create a new React project using Vite for an Authentication Screen.
Features:
1. Login Form with Email and Password.
2. Submit button.
3. Basic form validation (email format, password length).
4. Use TailwindCSS for styling.
5. Create a specific component for the LoginForm.
"""

async def run_verification():
    print(f"🚀 Starting React Auth Project Verification: {PROJECT_ID}")
    print(f"DEBUG: Analytics Enabled: {analytics.enabled}")
    print(f"DEBUG: Session Maker: {analytics.session_maker}")
    if not analytics.enabled:
        print("⚠️ Analytics DISABLED. Cannot verify DB.")
        return

    # Clean up previous run
    if os.path.exists(f".agentic/{PROJECT_ID}"):
        shutil.rmtree(f".agentic/{PROJECT_ID}")
    
    # Initialize Orchestrator
    orchestrator = OrchestratorAgent()
    
    task = {
        "mode": "autonomous",
        "user_prompt": USER_PROMPT,
        "project_id": PROJECT_ID,
        "model": "gpt-4o",
        "provider": "openai"
    }

    # Execute
    print("⏳ Executing Orchestrator (this may take a while)...")
    result = await orchestrator.execute(task)
    
    print("\n✅ Execution Finished")
    print(f"Status: {result.get('status')}")
    
    # Wait for async logs
    print("⏳ Waiting to ensure logs are flushed...")
    await asyncio.sleep(5)

    # Verify Files
    print("\n--- Verifying Generated Files ---")
    project_path = f"projects/{PROJECT_ID}" # Fallback path logic in code
    # Actual path check via ProjectManager would be better, but assuming default structure for now
    # The agent might create it in a different spot depending on config, but standard is projects/ID
    
    # We can assume the agent logs where it put it, but let's check standard locations
    possible_paths = [
        f"projects/{PROJECT_ID}/package.json",
        f"projects/{PROJECT_ID}/src/App.jsx",
        f"projects/{PROJECT_ID}/src/components/LoginForm.jsx",
        os.path.abspath(f"projects/{PROJECT_ID}/package.json")
    ]
    
    found_files = 0
    from coding_agent_plugin.managers import ProjectManager
    pm = ProjectManager()
    project = pm.get_project(PROJECT_ID)
    if project:
        base_path = project["storage_path"]
        print(f"Project Path: {base_path}")
        
        expected_files = ["package.json", "src/App.jsx", "src/components/LoginForm.jsx"]
        for f in expected_files:
            full_path = os.path.join(base_path, f)
            if os.path.exists(full_path):
                print(f"✅ Found file: {f}")
                found_files += 1
            else:
                 # It might be in a subfolder or different structure depending on how LLM behaved
                 print(f"⚠️ Missing file: {f} (Checking simple search)")
                 
    
    # Verify Analytics
    print("\n--- Verifying Analytics Data ---")
    async with analytics.session_maker() as session:
        # Check Agent Flow
        print("Checking Flow Events:")
        for action in ["ORCHESTRATOR_START", "PLANNING_START", "PLANNING_COMPLETE", "CODING_START", "CODING_COMPLETE", "ORCHESTRATOR_COMPLETE"]:
             res = await session.execute(text(
                f"SELECT count(*) FROM analytics_audit_log WHERE project_id = '{PROJECT_ID}' AND action = '{action}'"
            ))
             count = res.scalar()
             emoji = "✅" if count > 0 else "❌"
             print(f"{emoji} {action}: {count}")

        # Check Tokens
        res = await session.execute(text(
            f"SELECT sum(total_tokens), sum(cost_usd) FROM analytics_token_usage WHERE project_id = '{PROJECT_ID}'"
        ))
        tokens, cost = res.fetchone()
        if tokens and tokens > 0:
             print(f"✅ Total Tokens Used: {tokens}")
             print(f"💰 Total Cost: ${cost:.4f}")
        else:
             print("❌ No Token Usage Recorded")

if __name__ == "__main__":
    asyncio.run(run_verification())
