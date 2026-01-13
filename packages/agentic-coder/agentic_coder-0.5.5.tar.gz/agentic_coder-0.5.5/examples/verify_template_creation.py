import asyncio
import sys
import os
import shutil
from pathlib import Path

# Setup path
sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.services.template import TemplateService

async def verify_template():
    print("🚀 Verifying Template Service")
    
    test_dir = Path("examples/test_template_proj")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True)
    
    # 1. List Templates
    templates = TemplateService.list_templates()
    print(f"📋 Available Templates: {list(templates.keys())}")
    
    # 2. Apply 'python-fastapi'
    print("\nApplying 'python-fastapi'...")
    await TemplateService.apply_template("python-fastapi", test_dir)
    
    # 3. Verify files
    expected = ["app/main.py", "requirements.txt", "README.md"]
    for f in expected:
        if (test_dir / f).exists():
            print(f"✅ Created {f}")
        else:
            print(f"❌ Missing {f}")
            
    # Cleanup
    print("\nCleanup...")
    shutil.rmtree(test_dir)
    print("Done")

if __name__ == "__main__":
    asyncio.run(verify_template())
