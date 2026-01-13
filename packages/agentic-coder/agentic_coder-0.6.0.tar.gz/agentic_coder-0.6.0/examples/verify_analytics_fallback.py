import os
import sys

# Mock Environment: Analytics ON, DB MISSING
os.environ["ENABLE_ANALYTICS"] = "true"
if "POSTGRES_DB" in os.environ:
    del os.environ["POSTGRES_DB"]

sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.services.analytics import AnalyticsService

def verify_fallback():
    print("🚀 Verifying Analytics Fallback (Enabled=True, DB=None)")
    
    analytics = AnalyticsService()
    print(f"Analytics Object Created: {analytics}")
    print(f"Enabled Status: {analytics.enabled}")
    
    # It should interpret None as False-y
    if analytics.enabled:
        print("❌ Unexpected: Analytics is ENABLED despite missing DB")
    else:
        print("✅ Success: Analytics is DISABLED due to missing DB")
        
    if analytics.session_maker is None:
        print("✅ Session Maker is None")
    else:
        print("❌ Session Maker is initialized!")

if __name__ == "__main__":
    verify_fallback()
