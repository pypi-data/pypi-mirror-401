import asyncio
import os
import sys

# Set Envs BEFORE importing plugin modules
os.environ["ENABLE_ANALYTICS"] = "true"
os.environ["POSTGRES_DB"] = "postgresql+asyncpg://admin:admin@localhost:5432/coding_agent"

# Add src to path
sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.services.analytics import analytics
from sqlalchemy import text

async def verify_live_db():
    print(f"--- Live DB Verification ---")
    print(f"Target: {os.environ['POSTGRES_DB']}")
    
    # 1. Ensure Tables
    print("\n1. Running ensure_tables()...")
    try:
        await analytics.ensure_tables()
        print("✅ Tables ensured (created or existed).")
    except Exception as e:
        print(f"❌ Failed to ensure tables: {e}")
        return

    # 2. Track Usage
    print("\n2. Tracking Token Usage...")
    try:
        # GPT-4o: 1K input, 1K output ~ $0.02
        await analytics.track_token_usage(
            project_id="live_test_proj",
            model="gpt-4o",
            input_tokens=1000,
            output_tokens=1000,
            total_tokens=2000
        )
        print("✅ Token usage tracked.")
    except Exception as e:
         print(f"❌ Failed to track token usage: {e}")
         return

    # 3. Log Audit Action
    print("\n3. Logging Audit Action...")
    try:
        await analytics.log_action(
            project_id="live_test_proj",
            action="LIVE_TEST_ACTION",
            details={"msg": "This is a real DB test"}
        )
        print("✅ Audit action logged.")
    except Exception as e:
        print(f"❌ Failed to log audit action: {e}")
        return

    # 4. Verify Data via SQL
    print("\n4. Verifying Data in DB...")
    try:
        async with analytics.session_maker() as session:
            # Check Token Usage
            result_tok = await session.execute(text(
                "SELECT * FROM analytics_token_usage WHERE project_id = 'live_test_proj' ORDER BY id DESC LIMIT 1"
            ))
            row_tok = result_tok.fetchone()
            if row_tok:
                print(f"✅ Found Token Record: {row_tok.model}, Cost: ${row_tok.cost_usd}")
            else:
                print("❌ No Token Record found!")

            # Check Audit Log
            result_audit = await session.execute(text(
                "SELECT * FROM analytics_audit_log WHERE project_id = 'live_test_proj' ORDER BY id DESC LIMIT 1"
            ))
            row_audit = result_audit.fetchone()
            if row_audit:
                print(f"✅ Found Audit Record: {row_audit.action}, Details: {row_audit.details}")
            else:
                print("❌ No Audit Record found!")
                
    except Exception as e:
        print(f"❌ Verification Query Failed: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(verify_live_db())
    except KeyboardInterrupt:
        pass
