import asyncio
import os
import sys
import shutil

# Set Envs BEFORE importing plugin
os.environ["ENABLE_ANALYTICS"] = "true"
os.environ["POSTGRES_DB"] = "postgresql+asyncpg://admin:admin@localhost:5432/coding_agent"
# We need OpenAI Key for the agents to actually "think" (or we mock the LLM)
# Assuming LLM_API_KEY is in the user's environment or .env
# If not, the agents will fail. 
# For this test, if LLM fails, we at least see the START logs.

sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.services.analytics import analytics
from sqlalchemy import text

async def verify_live_project_run():
    project_id = "live_real_project"
    print(f"--- Live Project Run Verification ({project_id}) ---")
    
    # Clean up fs first
    if os.path.exists(f"/Users/abu/.agentic-coder/projects/{project_id}"):
        shutil.rmtree(f"/Users/abu/.agentic-coder/projects/{project_id}")

    # Initialize Analytics
    await analytics.ensure_tables()

    # Init Orchestrator
    try:
        orchestrator = OrchestratorAgent()
        print("✅ Orchestrator Initialized")
    except Exception as e:
        print(f"❌ Orchestrator Init Failed (Dependency issue?): {e}")
        return

    # Run Task
    print("🚀 Starting Autonomous Task...")
    task = {
        "mode": "autonomous",
        "user_prompt": "Create a file named hello_realtime.txt with content 'Verified Live Analytics'",
        "project_id": project_id,
        "model": "gpt-4o",
        "provider": "openai"
    }

    try:
        # This will drive the full loop: Planning -> Task -> Coding -> Execution
        result = await orchestrator.execute(task)
        print("✅ Task Execution Finished")
        print(f"Status: {result.get('status')}")
    except Exception as e:
        print(f"⚠️ Task Execution Failed (Expected if NO LLM Key): {e}")
        # We proceed to check logs anyway, because START events should be there.

    # Wait for background tasks (Token Tracking)
    print("⏳ Waiting for background tasks...")
    await asyncio.sleep(5)

    # Verify DB Logs
    print("\n--- Verifying Analytics Logs ---")
    async with analytics.session_maker() as session:
        # Dump all recent logs
        print("Dumping last 10 Audit Logs:")
        all_logs = await session.execute(text("SELECT * FROM analytics_audit_log ORDER BY id DESC LIMIT 10"))
        for row in all_logs:
            print(f"  [{row.timestamp}] {row.project_id} | {row.action} | {row.details}")

        # 1. Orchestrator Start
        res = await session.execute(text(
            f"SELECT * FROM analytics_audit_log WHERE project_id = '{project_id}' AND action = 'ORCHESTRATOR_START'"
        ))
        if res.fetchone():
            print("✅ ORCHESTRATOR_START found")
        else:
            print("❌ ORCHESTRATOR_START missing")

        # 2. Agent Execution (Specific Agents)
        agents_found = 0
        for agent_name in ["PLANNING", "CODING", "EXECUTION"]:
            res = await session.execute(text(
                f"SELECT * FROM analytics_audit_log WHERE project_id = '{project_id}' AND action = '{agent_name}_START'"
            ))
            rows = res.fetchall()
            if rows:
                print(f"✅ {agent_name}_START found ({len(rows)} events)")
                agents_found += 1
            else:
                print(f"❌ {agent_name}_START missing")
        
        if agents_found == 3:
            print("✅ All Agent Types Verified")
        else:
            print("❌ Some Agents Missing")

        # 3. Token Usage (Only if LLM actually ran)
        print("Dumping last 10 Token Records:")
        all_tokens = await session.execute(text("SELECT * FROM analytics_token_usage ORDER BY id DESC LIMIT 10"))
        for row in all_tokens:
            print(f"  [{row.timestamp}] {row.project_id} | {row.model} | {row.total_tokens} tokens | ${row.cost_usd}")

        res = await session.execute(text(
            f"SELECT * FROM analytics_token_usage WHERE project_id = '{project_id}'"
        ))
        tokens = res.fetchall()
        if tokens:
            print(f"✅ Token Usage found ({len(tokens)} records)")
            total_cost = sum(r.cost_usd for r in tokens)
            print(f"💰 Total Cost: ${total_cost:.4f}")
        else:
            print("⚠️ No tokens recorded (Did LLM run?)")

if __name__ == "__main__":
    # Load dotenv if available to get LLM keys
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(verify_live_project_run())
