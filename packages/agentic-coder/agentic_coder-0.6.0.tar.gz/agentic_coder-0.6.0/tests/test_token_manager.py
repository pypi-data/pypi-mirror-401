import pytest
from coding_agent_plugin.utils.token_manager import TokenManager

class TestTokenManager:
    
    @pytest.fixture
    def token_manager(self):
        return TokenManager(model_name="gpt-4o")

    def test_count_tokens(self, token_manager):
        text = "Hello, world!"
        count = token_manager.count_tokens(text)
        assert count > 0

    def test_truncate_text(self, token_manager):
        text = "This is a long sentence that should be truncated."
        # Estimate tokens ~10
        truncated = token_manager.truncate_text(text, max_tokens=2)
        assert token_manager.count_tokens(truncated) <= 2
        
    def test_fit_context_preserves_mandatory(self, token_manager):
        mandatory = "Important."
        optional = "Less important."
        # Huge limit
        result = token_manager.fit_context(mandatory, optional, max_total_tokens=100)
        assert result == mandatory + optional
        
    def test_fit_context_truncates_optional(self, token_manager):
        mandatory = "Keep this."
        optional = "Truncate this long optional text."
        mandatory_tokens = token_manager.count_tokens(mandatory)
        # Limit to mandatory + 1 token
        result = token_manager.fit_context(mandatory, optional, max_total_tokens=mandatory_tokens + 1)
        
        assert mandatory in result
        assert len(result) < len(mandatory + optional)
        assert token_manager.count_tokens(result) <= mandatory_tokens + 1

    def test_fit_context_drops_optional_if_needed(self, token_manager):
        mandatory = "Only room for this."
        optional = "No room for this."
        mandatory_tokens = token_manager.count_tokens(mandatory)
        
        result = token_manager.fit_context(mandatory, optional, max_total_tokens=mandatory_tokens)
        
        assert result == mandatory
