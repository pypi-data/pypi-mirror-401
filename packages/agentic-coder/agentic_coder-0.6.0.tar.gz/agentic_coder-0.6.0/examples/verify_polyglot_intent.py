import asyncio
import os
import sys

# Setup
sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.services.intent import IntentService

async def main():
    print("🚀 Verifying Universal Support Intents")
    
    prompts = [
        "Create a Go API for user management",
        "Build a high-performance Rust backend",
        "I need a Node.js express server with typescript",
        "Create a simple python script"
    ]
    
    for p in prompts:
        print(f"\nPrompt: '{p}'")
        analysis = await IntentService.analyze_intent(p)
        print(f"  Mode: {analysis.get('mode')}")
        print(f"  Template: {analysis.get('suggested_template')}")
        
if __name__ == "__main__":
    asyncio.run(main())
