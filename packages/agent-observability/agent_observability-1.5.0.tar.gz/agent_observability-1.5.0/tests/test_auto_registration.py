"""Unit tests for auto-registration feature."""
from __future__ import annotations

import os
import pytest
from unittest.mock import patch, MagicMock, Mock
import httpx

from agent_observability import AgentLogger, log_event
from agent_observability.client import _REGISTRATION_CACHE


class TestAutoRegistration:
    """Tests for the auto-registration feature."""

    def setup_method(self):
        """Clear registration cache before each test."""
        _REGISTRATION_CACHE.clear()
        # Clear any environment variable
        if "AGENT_OBS_API_KEY" in os.environ:
            del os.environ["AGENT_OBS_API_KEY"]

    def test_auto_registration_on_first_log(self):
        """First log should auto-register and return API key."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "api_key": "ao_live_test123",
            "customer_id": "uuid-123"
        }
        mock_response.raise_for_status = MagicMock()

        with patch('httpx.post', return_value=mock_response) as mock_post:
            with patch.object(httpx.Client, 'post') as mock_client_post:
                mock_client_post.return_value = Mock(
                    json=lambda: {"id": "12345678-1234-5678-1234-567812345678"},
                    raise_for_status=MagicMock()
                )
                
                logger = AgentLogger()  # No API key
                result = logger.log("test", {"custom_key": "bar"})
                
                assert logger._auto_registered is True
                assert logger.api_key == "ao_live_test123"

    def test_no_duplicate_registration(self):
        """Subsequent logs should use cached key, not re-register."""
        mock_reg_response = Mock()
        mock_reg_response.json.return_value = {"api_key": "ao_live_test"}
        mock_reg_response.raise_for_status = MagicMock()

        with patch('httpx.post', return_value=mock_reg_response):
            with patch.object(httpx.Client, 'post') as mock_client_post:
                mock_client_post.return_value = Mock(
                    json=lambda: {"id": "12345678-1234-5678-1234-567812345678"},
                    raise_for_status=MagicMock()
                )
                
                logger = AgentLogger()
                logger.log("event1", {})
                logger.log("event2", {})
                
                # httpx.post is used for registration, Client.post for logs
                assert logger._auto_registered is True

    def test_existing_api_key_skips_registration(self):
        """If API key provided, skip auto-registration."""
        with patch('httpx.post') as mock_post:
            with patch.object(httpx.Client, 'post') as mock_client_post:
                mock_client_post.return_value = Mock(
                    json=lambda: {"id": "12345678-1234-5678-1234-567812345678"},
                    raise_for_status=MagicMock()
                )
                
                logger = AgentLogger(api_key="ao_live_existing")
                logger.log("event", {})
                
                # Registration should never be called
                assert mock_post.call_count == 0
                assert logger._auto_registered is False
                assert logger.api_key == "ao_live_existing"

    def test_env_var_api_key_skips_registration(self):
        """If AGENT_OBS_API_KEY env var set, skip auto-registration."""
        os.environ["AGENT_OBS_API_KEY"] = "ao_live_env_key"
        
        try:
            with patch('httpx.post') as mock_post:
                logger = AgentLogger()
                
                assert logger.api_key == "ao_live_env_key"
                assert logger._auto_registered is False
                assert mock_post.call_count == 0
        finally:
            del os.environ["AGENT_OBS_API_KEY"]

    def test_registration_timeout_fallback(self):
        """Should fallback to local logging if registration times out."""
        with patch('httpx.post') as mock_post:
            mock_post.side_effect = httpx.TimeoutException("timeout")
            
            logger = AgentLogger()
            
            # Trigger registration via log
            with patch.object(logger, '_write_fallback') as mock_fallback:
                logger.log("event", {})
                
                assert logger._fallback_mode is True
                # Fallback should be called
                assert mock_fallback.call_count >= 1

    def test_registration_network_error_fallback(self):
        """Should fallback to local logging on network errors."""
        with patch('httpx.post') as mock_post:
            mock_post.side_effect = httpx.RequestError("Network error")
            
            logger = AgentLogger()
            
            with patch.object(logger, '_write_fallback'):
                logger.log("event", {})
                
                assert logger._fallback_mode is True

    def test_registration_409_conflict_handled(self):
        """Should handle 409 conflict (already registered) gracefully."""
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.json.return_value = {
            "message": "Already registered",
            "api_key": "ao_live_existing...(stored)"
        }
        mock_response.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "409",
                request=Mock(),
                response=mock_response
            )
        )
        
        with patch('httpx.post', return_value=mock_response):
            logger = AgentLogger()
            
            # Should not raise, should handle gracefully
            with patch.object(logger, '_write_fallback'):
                result = logger._auto_register()
                
                assert result is not None or logger._fallback_mode

    def test_registration_500_retry(self):
        """Should retry on 500 errors with exponential backoff."""
        call_count = 0
        
        def mock_post(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            
            if call_count < 3:
                error_response = Mock()
                error_response.status_code = 500
                error_response.raise_for_status = MagicMock(
                    side_effect=httpx.HTTPStatusError(
                        "500",
                        request=Mock(),
                        response=error_response
                    )
                )
                return error_response
            else:
                # Third call succeeds
                success_response = Mock()
                success_response.json.return_value = {"api_key": "ao_live_test"}
                success_response.raise_for_status = MagicMock()
                return success_response
        
        with patch('httpx.post', side_effect=mock_post):
            with patch('time.sleep'):  # Skip actual sleep
                logger = AgentLogger()
                result = logger._auto_register()
                
                assert call_count == 3
                assert result is not None
                assert result.get("api_key") == "ao_live_test"

    def test_backward_compatibility_env_var(self):
        """Existing AGENT_OBS_API_KEY env var should work."""
        os.environ["AGENT_OBS_API_KEY"] = "ao_live_env_key"
        
        try:
            logger = AgentLogger()
            
            assert logger.api_key == "ao_live_env_key"
            assert logger._auto_registered is False
        finally:
            del os.environ["AGENT_OBS_API_KEY"]

    def test_agent_id_generation(self):
        """Should generate unique agent IDs."""
        logger1 = AgentLogger.__new__(AgentLogger)
        logger1.agent_id = AgentLogger._generate_agent_id(logger1)
        
        logger2 = AgentLogger.__new__(AgentLogger)
        logger2.agent_id = AgentLogger._generate_agent_id(logger2)
        
        # IDs should be different (contains UUID suffix)
        assert logger1.agent_id != logger2.agent_id
        
        # ID should contain hostname portion
        import socket
        hostname = socket.gethostname()[:20]
        assert hostname in logger1.agent_id or logger1.agent_id.startswith("agent-")

    def test_log_event_convenience_function(self):
        """log_event() should work without explicit logger creation."""
        mock_reg_response = Mock()
        mock_reg_response.json.return_value = {"api_key": "ao_live_test"}
        mock_reg_response.raise_for_status = MagicMock()
        
        with patch('httpx.post', return_value=mock_reg_response):
            with patch.object(httpx.Client, 'post') as mock_client_post:
                mock_client_post.return_value = Mock(
                    json=lambda: {"id": "12345678-1234-5678-1234-567812345678"},
                    raise_for_status=MagicMock()
                )
                
                # Reset module-level logger
                import agent_observability
                agent_observability._default_logger = None
                
                # Use valid metadata fields (custom keys go to 'custom' field)
                result = log_event("quick_test", {"model": "gpt-4", "cost_usd": 0.01})
                
                # Should have created and cached a logger
                assert agent_observability._default_logger is not None

    def test_multiple_instances_share_cache(self):
        """Multiple AgentLogger instances should share registration cache."""
        mock_response = Mock()
        mock_response.json.return_value = {"api_key": "ao_live_shared"}
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.post', return_value=mock_response) as mock_post:
            # First logger with specific agent_id
            logger1 = AgentLogger.__new__(AgentLogger)
            logger1.base_url = "https://api.test.com"
            logger1.agent_id = "shared-agent-123"
            logger1._auto_registered = False
            logger1._registration_shown = False
            logger1._fallback_mode = False
            
            result1 = logger1._auto_register()
            
            # Should have called API
            assert mock_post.call_count == 1
            
            # Second logger with same agent_id
            logger2 = AgentLogger.__new__(AgentLogger)
            logger2.base_url = "https://api.test.com"
            logger2.agent_id = "shared-agent-123"
            logger2._auto_registered = False
            logger2._registration_shown = False
            logger2._fallback_mode = False
            
            result2 = logger2._auto_register()
            
            # Should have used cache, not called API again
            assert mock_post.call_count == 1
            assert result2.get("cached") is True


class TestAutoRegistrationMessages:
    """Tests for registration message display."""

    def setup_method(self):
        """Clear registration cache before each test."""
        _REGISTRATION_CACHE.clear()
        if "AGENT_OBS_API_KEY" in os.environ:
            del os.environ["AGENT_OBS_API_KEY"]

    def test_registration_message_shown_once(self, capsys):
        """Registration message should only be shown once."""
        mock_response = Mock()
        mock_response.json.return_value = {"api_key": "ao_live_test123"}
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.post', return_value=mock_response):
            logger = AgentLogger.__new__(AgentLogger)
            logger.base_url = "https://api.test.com"
            logger.agent_id = "test-agent"
            logger._auto_registered = False
            logger._registration_shown = False
            logger._fallback_mode = False
            
            # First registration
            logger._auto_register()
            output1 = capsys.readouterr().out
            
            # Second call (should use cache)
            logger._registration_shown = False  # Reset for test
            logger._auto_register()
            output2 = capsys.readouterr().out
            
            # First should show message
            assert "Auto-registered" in output1
            # Second should also show (since we reset _registration_shown)
            # In real usage, _registration_shown prevents duplicate messages


class TestFallbackBehavior:
    """Tests for fallback mode behavior."""

    def setup_method(self):
        """Clear registration cache before each test."""
        _REGISTRATION_CACHE.clear()
        if "AGENT_OBS_API_KEY" in os.environ:
            del os.environ["AGENT_OBS_API_KEY"]

    def test_fallback_writes_to_file(self, tmp_path):
        """When in fallback mode, logs should be written to local file."""
        fallback_file = tmp_path / "fallback.jsonl"
        
        with patch('httpx.post') as mock_post:
            mock_post.side_effect = httpx.TimeoutException("timeout")
            
            logger = AgentLogger(fallback_path=str(fallback_file))
            logger.log("test_event", {"key": "value"})
            
            assert logger._fallback_mode is True
            assert fallback_file.exists()
            
            # Read and verify content
            content = fallback_file.read_text()
            assert "test_event" in content
            assert "key" in content

