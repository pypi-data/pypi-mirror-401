import asyncio
import os
import shutil
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.services.template import TemplateService
from coding_agent_plugin.services.quality import QualityService

TEST_ROOT = Path("temp_polyglot_test")

async def test_stack(name: str, template: str, check_file: str, format_ext: str = None):
    print(f"\n[Testing {name.upper()} Stack]")
    project_dir = TEST_ROOT / name
    
    # 1. Cleanup & Create
    if project_dir.exists():
        shutil.rmtree(project_dir)
    project_dir.mkdir(parents=True)
    
    print(f"  📂 Created dir: {project_dir}")
    
    # 2. Apply Template
    print(f"  🛠️ Applying template: {template}...")
    try:
        await TemplateService.apply_template(template, project_dir)
        print("  ✅ Template applied successfully")
    except Exception as e:
        print(f"  ❌ Template application failed: {e}")
        return

    # 3. Check Files
    target_file = project_dir / check_file
    if target_file.exists():
        print(f"  ✅ Verified file exists: {check_file}")
    else:
        print(f"  ❌ Missing expected file: {check_file}")
        return

    # 4. Check Formatting
    if format_ext:
        print(f"  🎨 Testing Quality Gate ({format_ext})...")
        # Find a file to format
        files = list(project_dir.glob(f"**/*{format_ext}"))
        if files:
            test_file = files[0]
            if QualityService.format_file(test_file):
                 print(f"  ✅ Formatting successful for: {test_file.name}")
            else:
                 print(f"  ⚠️ Formatting failed (Tool missing?) for: {test_file.name}")
        else:
             print("  ⚠️ No matching files found to format")

async def main():
    print("🚀 STARTING BIG POLYGLOT TEST")
    
    if TEST_ROOT.exists():
        shutil.rmtree(TEST_ROOT)
        
    await test_stack("python_app", "python-fastapi", "app/main.py", ".py")
    await test_stack("go_app", "go-gin", "main.go", ".go")
    await test_stack("rust_app", "rust-actix", "Cargo.toml", ".rs")
    await test_stack("node_app", "express-api", "package.json", ".ts")
    
    print("\n🧹 Cleanup...")
    # shutil.rmtree(TEST_ROOT) # Keep it for inspection if user wants
    print(f"Tests Completed. Artifacts left in {TEST_ROOT}")

if __name__ == "__main__":
    asyncio.run(main())
