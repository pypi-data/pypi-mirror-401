"""Tests for request timeout handling (Bandit B113 security fix)."""
import logging
import unittest
from unittest.mock import MagicMock, Mock, patch

import requests

from vss_cli.config import Configuration
from vss_cli.exceptions import VssCliError


class TestAssistantAPITimeouts(unittest.TestCase):
    """Test suite for assistant API timeout handling in config.py."""

    def setUp(self):
        """Set up test configuration."""
        self.config = Configuration()
        self.config.gpt_server = 'http://test-server'
        self.config.gpt_persona = 1
        self.config._gpt_persona = 1
        self.config.debug = False
        self.config.user_agent = 'test-agent/1.0'

    def test_generate_assistant_api_key_timeout_raises_vss_cli_error(self):
        """Test that _generate_assistant_api_key() raises VssCliError on timeout."""
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock a timeout exception
            mock_post.side_effect = requests.exceptions.Timeout(
                "Connection timed out"
            )

            # Verify VssCliError is raised with appropriate message
            with self.assertRaises(VssCliError) as context:
                self.config._generate_assistant_api_key()

            self.assertIn(
                "Request to generate assistant API key timed out",
                str(context.exception),
            )
            self.assertIn(
                "service may be temporarily unavailable",
                str(context.exception),
            )

    def test_get_new_chat_id_timeout_raises_vss_cli_error(self):
        """Test that get_new_chat_id() raises VssCliError on timeout."""
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock a timeout exception
            mock_post.side_effect = requests.exceptions.Timeout(
                "Connection timed out"
            )

            # Verify VssCliError is raised with appropriate message
            with self.assertRaises(VssCliError) as context:
                self.config.get_new_chat_id(
                    chat_endpoint='http://test/api/chat/create-chat-session',
                    persona_id=1,
                    description='test',
                    headers={'api-key': 'test-key'},
                )

            self.assertIn(
                "Request to create chat session timed out",
                str(context.exception),
            )
            self.assertIn(
                "service may be temporarily unavailable",
                str(context.exception),
            )

    def test_provide_assistant_feedback_timeout_returns_false(self):
        """Test that provide_assistant_feedback() returns False on timeout."""
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock a timeout exception
            mock_post.side_effect = requests.exceptions.Timeout(
                "Connection timed out"
            )

            # Verify method returns False on timeout
            result = self.config.provide_assistant_feedback(
                chat_message_id='123',
                api_key='test-api-key',
                is_positive=True,
                feedback_text='Great response!',
            )

            self.assertFalse(result)

    def test_successful_requests_work_with_timeout_parameter(self):
        """Test that successful requests work correctly with timeout parameter."""
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock successful response for API key generation
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.status_code = 200
            mock_response.json.return_value = {'api_key': 'generated-key'}
            mock_post.return_value = mock_response

            # Call _generate_assistant_api_key
            result = self.config._generate_assistant_api_key()

            # Verify timeout parameter was passed
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            self.assertIn('timeout', call_kwargs)
            self.assertEqual(call_kwargs['timeout'], 30)  # DEFAULT_TIMEOUT

            # Verify the result
            self.assertEqual(result, 'generated-key')


class TestExternalStatusCheckTimeouts(unittest.TestCase):
    """Test suite for external status check timeout handling."""

    def test_hcio_check_status_returns_unknown_on_timeout(self):
        """Test that hcio.check_status() returns 'unknown' status on timeout."""
        with patch('vss_cli.hcio.requests.get') as mock_get:
            # Mock a timeout exception
            mock_get.side_effect = requests.exceptions.Timeout(
                "Connection timed out"
            )

            from vss_cli import hcio

            result = hcio.check_status()

            # Verify unknown status is returned
            self.assertEqual(result['status'], 'unknown')
            self.assertEqual(result['name'], 'ITS Private Cloud API')

    def test_sstatus_get_component_returns_none_on_timeout(self):
        """Test that sstatus.get_component() returns None on timeout."""
        with patch('vss_cli.sstatus.requests.get') as mock_get:
            # Mock a timeout exception
            mock_get.side_effect = requests.exceptions.Timeout(
                "Connection timed out"
            )

            from vss_cli import sstatus

            result = sstatus.get_component()

            # Verify None is returned
            self.assertIsNone(result)

    def test_sstatus_get_upcoming_maintenance_returns_empty_list_on_timeout(
        self,
    ):
        """Test that get_upcoming_maintenance_by_service() returns [] on timeout."""
        with patch('vss_cli.sstatus.requests.get') as mock_get:
            # Mock a timeout exception
            mock_get.side_effect = requests.exceptions.Timeout(
                "Connection timed out"
            )

            from vss_cli import sstatus

            result = sstatus.get_upcoming_maintenance_by_service()

            # Verify empty list is returned
            self.assertEqual(result, [])

    def test_successful_external_requests_work_with_timeout(self):
        """Test that successful external requests work with timeout parameter."""
        with patch('vss_cli.hcio.requests.get') as mock_get:
            # Mock successful response
            mock_response = MagicMock()
            mock_response.json.return_value = {'status': 'up'}
            mock_get.return_value = mock_response

            from vss_cli import hcio

            result = hcio.check_status()

            # Verify timeout parameter was passed
            mock_get.assert_called_once()
            call_kwargs = mock_get.call_args[1]
            self.assertIn('timeout', call_kwargs)
            self.assertEqual(call_kwargs['timeout'], 10)

            # Verify the result
            self.assertEqual(result['status'], 'operational')


class TestTimeoutConfigurationFallback(unittest.TestCase):
    """Test suite for timeout configuration value fallback behavior."""

    def test_custom_timeout_value_is_used_when_set(self):
        """Test that self.timeout value is used when configured."""
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.user_agent = 'test-agent/1.0'
        config.timeout = 60  # Custom timeout value

        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock successful response
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.status_code = 200
            mock_response.json.return_value = {'api_key': 'generated-key'}
            mock_post.return_value = mock_response

            # Call _generate_assistant_api_key
            config._generate_assistant_api_key()

            # Verify custom timeout was used
            call_kwargs = mock_post.call_args[1]
            self.assertEqual(call_kwargs['timeout'], 60)

    def test_default_timeout_used_when_self_timeout_is_none(self):
        """Test that DEFAULT_TIMEOUT is used when self.timeout is None."""
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.user_agent = 'test-agent/1.0'
        config.timeout = None  # Explicit None

        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock successful response
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.status_code = 200
            mock_response.json.return_value = {'api_key': 'generated-key'}
            mock_post.return_value = mock_response

            # Call _generate_assistant_api_key
            config._generate_assistant_api_key()

            # Verify DEFAULT_TIMEOUT (30) was used
            call_kwargs = mock_post.call_args[1]
            self.assertEqual(call_kwargs['timeout'], 30)


if __name__ == '__main__':
    unittest.main()
