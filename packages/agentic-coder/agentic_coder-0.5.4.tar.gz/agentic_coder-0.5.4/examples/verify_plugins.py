
import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath("src"))

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

def verify_agent_loading():
    print("🔌 Verifying Dynamic Agent Loading...")
    
    try:
        orchestrator = OrchestratorAgent()
        agents = orchestrator.agents
        
        print(f"✅ Orchestrator initialized.")
        print(f"📂 Loaded Agents: {list(agents.keys())}")
        
        expected_agents = ["planning", "coding", "task", "error", "execution"]
        missing = [a for a in expected_agents if a not in agents]
        
        if missing:
            print(f"❌ Verification FAILED. Missing agents: {missing}")
            sys.exit(1)
            
        print("✨ Verification PASSED. All core agents loaded dynamically.")
        
    except Exception as e:
        print(f"❌ Verification FAILED with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_agent_loading()
