import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath("src"))
# Mock envs if needed
os.environ["ENABLE_ANALYTICS"] = "false" # Skip analytics to avoid DB connection in this unit test

from coding_agent_plugin.services.intent import IntentService

async def verify_intent():
    print("🚀 Verifying Intent Service")
    
    scenarios = [
        "Create a react app for a dashboard",
        "Write a python script to calculate fibonacci",
        "Create a backend using fastapi",
        "Fix the sorting bug in util.py",
        "I need a Next.js landing page"
    ]
    
    for prompt in scenarios:
        print(f"\nPrompt: '{prompt}'")
        try:
            result = await IntentService.analyze_intent(prompt)
            print(f"  Mode: {result.get('mode')}")
            print(f"  Template: {result.get('suggested_template')}")
            print(f"  Reason: {result.get('reasoning')}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    # Ensure LLM key is present or mocked?
    # We assume env is set.
    from dotenv import load_dotenv
    load_dotenv()
    
    asyncio.run(verify_intent())
