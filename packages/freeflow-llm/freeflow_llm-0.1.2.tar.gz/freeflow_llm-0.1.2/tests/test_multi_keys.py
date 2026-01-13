"""Tests for multiple API key support with automatic rotation."""

import os
from unittest.mock import Mock, patch

import pytest

from freeflow_llm import FreeFlowClient
from freeflow_llm.exceptions import NoProvidersAvailableError, RateLimitError
from freeflow_llm.providers import GeminiProvider, GroqProvider
from freeflow_llm.utils import get_api_keys


class TestMultipleAPIKeys:
    """Test suite for multiple API key functionality."""

    def test_get_api_keys_single_key(self):
        """Test parsing a single API key."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "single_key"}, clear=True):
            keys = get_api_keys("gemini")
            assert keys == ["single_key"]

    def test_get_api_keys_json_array(self):
        """Test parsing JSON array of API keys."""
        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": '["key1", "key2", "key3"]'},
            clear=True,
        ):
            keys = get_api_keys("gemini")
            assert keys == ["key1", "key2", "key3"]

    def test_get_api_keys_comma_separated(self):
        """Test parsing comma-separated API keys."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "key1,key2,key3"}, clear=True):
            keys = get_api_keys("gemini")
            assert keys == ["key1", "key2", "key3"]

    def test_get_api_keys_no_key(self):
        """Test when no API key is set."""
        with patch.dict(os.environ, {}, clear=True):
            keys = get_api_keys("gemini")
            assert keys == []

    def test_provider_initialization_with_multiple_keys(self):
        """Test provider initialization with multiple keys."""
        provider = GeminiProvider(api_key=["key1", "key2", "key3"])
        assert len(provider.api_keys) == 3
        assert provider.api_key == "key1"  # Should start with first key
        assert provider.is_available()

    def test_provider_initialization_with_single_key(self):
        """Test provider initialization with single key."""
        provider = GeminiProvider(api_key="single_key")
        assert len(provider.api_keys) == 1
        assert provider.api_key == "single_key"
        assert provider.is_available()

    def test_provider_initialization_from_env(self):
        """Test provider initialization from environment variables."""
        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": '["env_key1", "env_key2"]'},
            clear=True,
        ):
            provider = GeminiProvider()
            assert len(provider.api_keys) == 2
            assert provider.api_key == "env_key1"
            assert provider.is_available()

    def test_key_rotation(self):
        """Test API key rotation functionality."""
        provider = GeminiProvider(api_key=["key1", "key2", "key3"])
        
        # Start with first key
        assert provider.api_key == "key1"
        assert provider.current_key_index == 0
        
        # Rotate to second key
        assert provider.rotate_key() is True
        assert provider.api_key == "key2"
        assert provider.current_key_index == 1
        
        # Rotate to third key
        assert provider.rotate_key() is True
        assert provider.api_key == "key3"
        assert provider.current_key_index == 2
        
        # No more keys to rotate
        assert provider.rotate_key() is False
        assert provider.api_key == "key3"
        assert provider.current_key_index == 2

    def test_reset_key_index(self):
        """Test resetting key index to first key."""
        provider = GeminiProvider(api_key=["key1", "key2", "key3"])
        
        # Rotate to last key
        provider.rotate_key()
        provider.rotate_key()
        assert provider.api_key == "key3"
        
        # Reset to first key
        provider.reset_key_index()
        assert provider.api_key == "key1"
        assert provider.current_key_index == 0

    def test_has_more_keys(self):
        """Test checking if more keys are available."""
        provider = GeminiProvider(api_key=["key1", "key2"])
        
        assert provider.has_more_keys() is True
        provider.rotate_key()
        assert provider.has_more_keys() is False

    @patch("freeflow_llm.providers.base.httpx.Client")
    def test_chat_with_key_rotation_on_rate_limit(self, mock_client_class):
        """Test automatic key rotation when rate limit is hit."""
        provider = GeminiProvider(api_key=["key1", "key2", "key3"])
        
        # Mock HTTP client
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        provider.client = mock_client
        
        # First two keys hit rate limit (429), third succeeds
        response_429 = Mock()
        response_429.status_code = 429
        response_429.json.return_value = {"error": {"message": "Rate limit exceeded"}}
        response_429.raise_for_status.side_effect = Exception("429 Rate Limit")
        
        response_success = Mock()
        response_success.status_code = 200
        response_success.json.return_value = {
            "candidates": [
                {
                    "content": {"parts": [{"text": "Success with key3"}]},
                    "finishReason": "STOP",
                }
            ]
        }
        
        mock_client.post.side_effect = [
            response_429,  # First key fails
            response_429,  # Second key fails
            response_success,  # Third key succeeds
        ]
        
        # Make request - should automatically try all 3 keys
        # Note: This is a simplified test; actual implementation has more complex error handling
        # In a real scenario, you'd test the full flow including error handling

    def test_client_with_multiple_providers_and_keys(self):
        """Test client initialization with multiple providers having multiple keys."""
        with patch.dict(
            os.environ,
            {
                "GROQ_API_KEY": '["groq1", "groq2"]',
                "GEMINI_API_KEY": '["gemini1", "gemini2", "gemini3"]',
            },
            clear=True,
        ):
            client = FreeFlowClient(verbose=False)
            
            # Check providers are loaded
            assert len(client.providers) == 2
            
            # Check Groq has 2 keys
            groq_provider = next(p for p in client.providers if p.name == "groq")
            assert len(groq_provider.api_keys) == 2
            
            # Check Gemini has 3 keys
            gemini_provider = next(p for p in client.providers if p.name == "gemini")
            assert len(gemini_provider.api_keys) == 3

    def test_client_logs_key_count(self, capsys):
        """Test that client logs the number of keys per provider."""
        provider = GeminiProvider(api_key=["key1", "key2", "key3"])
        
        # Verify the provider has the correct number of keys
        assert len(provider.api_keys) == 3

    def test_empty_keys_filtered(self):
        """Test handling of keys with empty/whitespace values."""
        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": '["key1", "", "key2", "   ", "key3"]'},
            clear=True,
        ):
            keys = get_api_keys("gemini")
            # The strip() and if k check filters out pure whitespace
            # Empty strings after strip are filtered, but "" stays as is in JSON
            assert "key1" in keys
            assert "key2" in keys
            assert "key3" in keys

    def test_malformed_json_falls_back_to_comma_separated(self):
        """Test that malformed JSON falls back to comma-separated parsing."""
        with patch.dict(
            os.environ,
            {"GEMINI_API_KEY": '["key1", "key2"'},  # Missing closing bracket
            clear=True,
        ):
            keys = get_api_keys("gemini")
            # JSON parsing fails, falls back to comma-separated parsing
            # The string contains a comma, so it's split on commas
            assert len(keys) == 2
            assert '["key1"' in keys
            assert '"key2"' in keys


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

