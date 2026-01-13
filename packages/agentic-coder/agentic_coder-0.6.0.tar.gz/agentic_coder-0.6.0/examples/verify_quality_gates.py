import os
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.services.quality import QualityService

def verify_quality():
    print("🚀 Verifying Quality Service (Black/Prettier)")
    
    # 1. Test Python Formatting
    dirty_py = "def foo():\n  x = [ 1, 2,3]\n  return x"
    py_path = Path("dirty_test.py")
    py_path.write_text(dirty_py)
    
    print("\n[Before Format]")
    print(py_path.read_text())
    
    if QualityService.format_file(py_path):
        print("\n✅ Python Formatting Success")
        formatted = py_path.read_text()
        print("[After Format]")
        print(formatted)
        if "x = [1, 2, 3]" in formatted:
             print("✅ Style check passes (Black)")
        else:
             print("❌ Style check falied")
    else:
        print("\n❌ Python Formatting Failed")
        
    py_path.unlink()
    
    # 2. Test JS Formatting (Optional)
    dirty_js = "function test() {console.log('hello')}"
    js_path = Path("dirty_test.js")
    js_path.write_text(dirty_js)
    
    print("\n[Before Format JS]")
    print(js_path.read_text())
    
    if QualityService.format_file(js_path):
        print("\n✅ JS Formatting Success")
        print("[After Format JS]")
        print(js_path.read_text())
    else:
        print("\n⚠️ JS Formatting Skipped/Failed (Expected if prettier not installed)")

    js_path.unlink()

if __name__ == "__main__":
    verify_quality()
