
import asyncio
import os
import sys

# Ensure src is in path for "local plugin" usage simulation
sys.path.append(os.path.abspath("src"))

from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.agents.orchestrator import OrchestratorAgent

async def run_interactive_session():
    print("🤖 Agentic Coder - Realtime User Simulation")
    print("==========================================")
    
    # 1. Initialize
    pm = ProjectManager()
    project_name = "ecommerce-backend-simulation"
    
    # Check if exists
    project = pm.get_project(project_name)
    if not project:
        print(f"📦 Creating new project: {project_name}")
        project = pm.create_project(project_name, "Simulated E-commerce Backend")
    else:
        print(f"📂 Using existing project: {project_name}")
        
    project_id = project['id']
    orchestrator = OrchestratorAgent()
    
    # 2. Initial Prompt (A-Z)
    print("\n📝 Initial Request: Create a production-ready A-Z E-commerce Backend")
    print("(FastAPI, SQLAlchemy, Docker, JWT Auth, Products, Orders)")
    
    # Run the base project
    # In a real "A-Z" scenario, this takes time. We assume the orchestrator handles it.
    await orchestrator.run_project(
        user_prompt="Create a production-ready E-commerce backend with FastAPI, SQLAlchemy (SQLite for demo), Docker, and JWT Auth. Include Products and Orders modules.",
        project_id=project_id
    )
    
    # 3. Interactive Loop
    print("\n✨ Base project creation attempts completed.")
    print("💬 Entering Interactive Mode. Type your instructions (or 'exit' to quit).")
    
    while True:
        try:
            user_input = input("\n👤 User > ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("👋 Exiting simulation.")
                break
            
            if not user_input.strip():
                continue
                
            print(f"🤖 Agent > Processing: {user_input}")
            
            # For incremental updates, we also use run_project but with specific instructions
            # The PlanningAgent (if smart) will see existing files and add to them.
            result = await orchestrator.run_project(
                user_prompt=user_input,
                project_id=project_id
            )
            
            status = result.get("status", "unknown")
            print(f"✅ Finished task batch. Status: {status}")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_interactive_session())
    except KeyboardInterrupt:
        pass
