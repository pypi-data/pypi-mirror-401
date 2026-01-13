import asyncio
import os
import shutil
import json
import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from pathlib import Path

# Set setup to ensure we use local source
import sys
sys.path.insert(0, os.path.abspath("src"))

from coding_agent_plugin.managers import ProjectManager
from coding_agent_plugin.services.analytics import AnalyticsService

class TestSystemArchitecture(unittest.TestCase):
    
    def setUp(self):
        self.test_id = "test_verification_project"
        self.pm = ProjectManager()
        # Cleanup before test
        self.pm.delete_project(self.test_id)

    def tearDown(self):
        # Cleanup after test
        self.pm.delete_project(self.test_id)

    def test_fs_project_lifecycle(self):
        print("\n--- Testing FS Project Lifecycle ---")
        
        # 1. Create
        print(f"Creating project '{self.test_id}'...")
        proj = self.pm.create_project(self.test_id, "Description for verification")
        self.assertEqual(proj["name"], self.test_id)
        self.assertTrue(os.path.exists(proj["storage_path"]))
        
        # 2. Verify JSON Metadata
        config_path = Path(proj["storage_path"]) / ".agentic" / "config.json"
        self.assertTrue(config_path.exists(), "Config file missing")
        
        metadata = json.loads(config_path.read_text())
        self.assertEqual(metadata["name"], self.test_id)
        print("✅ Metadata verified on disk")
        
        # 3. List
        print("Listing projects...")
        projects = self.pm.list_projects()
        found = any(p["name"] == self.test_id for p in projects)
        self.assertTrue(found, "Project not found in list")
        print("✅ Project listed successfully")
        
        # 4. Get by ID and Name
        got_by_name = self.pm.get_project(self.test_id)
        self.assertIsNotNone(got_by_name)
        
        got_by_id = self.pm.get_project(proj["id"])
        self.assertIsNotNone(got_by_id)
        print("✅ Project retrieval verified (ID and Name)")

    @patch("coding_agent_plugin.services.analytics.create_async_engine")
    def test_analytics_enabled_behavior(self, mock_create_engine):
        print("\n--- Testing Analytics (Enabled) ---")
        
        # Patch the module-level variables directly since they are already imported
        with patch("coding_agent_plugin.services.analytics.ENABLE_ANALYTICS", True), \
             patch("coding_agent_plugin.services.analytics.POSTGRES_DB", "postgresql+asyncpg://mock:5432/db"):
            
            # Resetting singleton for test
            AnalyticsService._instance = None
            service = AnalyticsService()
            
            self.assertTrue(service.enabled)
            mock_create_engine.assert_called_once()
            print("✅ Analytics enabled correctly")
            
            # Test track_token_usage
            mock_session = AsyncMock()
            service.session_maker = MagicMock(return_value=mock_session)
            
            # We need to mock the async context manager on session_maker call
            # session_maker() returns a session object
            # async with session_maker() -> session
            mock_session.__aenter__.return_value = mock_session
            
            asyncio.run(service.track_token_usage("proj1", "gpt-4", 10, 10, 20, 0.05))
            
            # Verify execute was called (INSERT statement)
            mock_session.execute.assert_called_once()
            print("✅ track_token_usage attempted DB insert")

    def test_cost_calculation(self):
        print("\n--- Testing Cost Calculation ---")
        AnalyticsService._instance = None
        service = AnalyticsService()
        
        # Test GPT-4o pricing (Input $5 / Output $15 per 1M)
        cost = service.calculate_cost("gpt-4o", 1_000_000, 1_000_000)
        self.assertAlmostEqual(cost, 20.00)
        print(f"✅ GPT-4o Cost (1M/1M): ${cost} (Expected $20.00)")
        
        # Test Default (Zero)
        cost = service.calculate_cost("unknown-model", 100, 100)
        self.assertEqual(cost, 0.0)
        print(f"✅ Unknown Model Cost: ${cost} (Expected $0.0)")

        cost = service.calculate_cost("unknown-model", 100, 100)
        self.assertEqual(cost, 0.0)
        print(f"✅ Unknown Model Cost: ${cost} (Expected $0.0)")

    @patch("coding_agent_plugin.services.analytics.create_async_engine")
    def test_all_agent_tracking(self, mock_engine):
        print("\n--- Testing All-Agent Tracking (InProcessACPClient) ---")
        
        # Mock external acp_sdk since it might not be installed in test env
        # We need to mock 'acp_sdk.models.models' specifically because of standard import behavior
        mock_acp = MagicMock()
        mock_models = MagicMock()
        mock_models_pkg = MagicMock()
        mock_models_pkg.models = mock_models
        
        modules = {
            "acp_sdk": mock_acp, 
            "acp_sdk.client": MagicMock(),
            "acp_sdk.models": mock_models_pkg,
            "acp_sdk.models.models": mock_models
        }
        
        with patch.dict(sys.modules, modules):
            from coding_agent_plugin.acp.client import InProcessACPClient
            
            # Mock Analytics Instance Global
            mock_analytics_instance = MagicMock()
            mock_analytics_instance.log_action = AsyncMock()
            
            with patch("coding_agent_plugin.services.analytics.ENABLE_ANALYTICS", True), \
                 patch("coding_agent_plugin.services.analytics.POSTGRES_DB", "postgresql+asyncpg://mock:5432/db"), \
                 patch("coding_agent_plugin.services.analytics.analytics", mock_analytics_instance):
            
                 # Mock Agent
                 mock_agent = AsyncMock()
                 mock_agent.execute.return_value = {"status": "success"}
                 
                 client = InProcessACPClient(agents={"test_agent": mock_agent})
                 
                 # Execute
                 asyncio.run(client.send_to_agent("test_agent", {"project_id": "p1", "msg": "hi"}))
                 
                 # Verify Logs: START, COMPLETE
                 # We check calls to the mocked analytics instance
                 self.assertEqual(mock_analytics_instance.log_action.call_count, 2)
                 
                 calls = mock_analytics_instance.log_action.call_args_list
                 start_call = calls[0]
                 complete_call = calls[1]
                 
                 self.assertEqual(start_call[0][1], "AGENT_EXECUTION_START")
                 self.assertEqual(complete_call[0][1], "AGENT_EXECUTION_COMPLETE")

                 print("✅ InProcessACPClient logged START and COMPLETE events")

    def test_analytics_disabled_behavior(self):
        print("\n--- Testing Analytics (Disabled) ---")
        
        # Mock Environment
        with patch.dict(os.environ, {"ENABLE_ANALYTICS": "false"}):
            AnalyticsService._instance = None
            service = AnalyticsService()
            
            self.assertFalse(service.enabled)
            self.assertIsNone(service.engine)
            
            # Call method, should be no-op
            # Using asynciorun to call async method
            asyncio.run(service.track_token_usage("proj1", "model", 0, 0, 0))
            print("✅ Disabled analytics causes 0 side effects")

if __name__ == "__main__":
    unittest.main()
