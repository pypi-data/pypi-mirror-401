"""Tests for the Onyx Chat Endpoint Migration.

This test module validates the migration from the deprecated
/api/chat/send-message endpoint to the new /api/chat/send-chat-message
endpoint.

Migration Deadline: February 1st, 2026
"""
import json
import unittest
from unittest.mock import MagicMock, Mock, patch

from vss_cli.config import Configuration


class TestEndpointMigration(unittest.TestCase):
    """Test suite for Task Group 1: Endpoint Migration (API Layer)."""

    def setUp(self):
        """Set up test configuration."""
        self.config = Configuration()
        self.config.gpt_server = 'http://test-server'
        self.config.gpt_persona = 1
        self.config._gpt_persona = 1
        self.config.debug = False
        self.config._generate_assistant_api_key = Mock(return_value='test-key')
        self.config.get_new_chat_id = Mock(return_value=123)
        self.config.smooth_print = Mock()
        self.config.clear_console = Mock()

    def test_requests_sent_to_new_endpoint(self):
        """Test that requests are sent to /api/chat/send-chat-message endpoint."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify the new endpoint URL is used
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            endpoint_url = call_args[0][0]
            self.assertEqual(
                endpoint_url,
                'http://test-server/api/chat/send-chat-message',
                "Endpoint should be /api/chat/send-chat-message",
            )

    def test_payload_includes_stream_parameter(self):
        """Test that payload includes stream: True parameter."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify payload contains stream: True
            call_kwargs = mock_post.call_args[1]
            payload = call_kwargs.get('json', {})
            self.assertIn('stream', payload)
            self.assertTrue(
                payload['stream'], "Payload should include stream: True"
            )

    def test_existing_payload_fields_preserved(self):
        """Test that existing payload fields are preserved unchanged."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify existing payload fields
            call_kwargs = mock_post.call_args[1]
            payload = call_kwargs.get('json', {})

            # Check chat_session_id is present
            self.assertIn('chat_session_id', payload)
            self.assertEqual(payload['chat_session_id'], 123)

            # Check message is present
            self.assertIn('message', payload)
            self.assertIn('test message', payload['message'])

            # Check parent_message_id is present
            self.assertIn('parent_message_id', payload)
            self.assertIsNone(payload['parent_message_id'])

    def test_streaming_response_properly_initiated(self):
        """Test that streaming response is properly initiated."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify stream=True is passed to requests.post
            call_kwargs = mock_post.call_args[1]
            self.assertTrue(
                call_kwargs.get('stream'),
                "requests.post should be called with stream=True",
            )

    def test_no_extra_optional_parameters_in_payload(self):
        """Test that no extra optional parameters are added to payload."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify no extra optional parameters
            call_kwargs = mock_post.call_args[1]
            payload = call_kwargs.get('json', {})

            # These parameters should NOT be present
            optional_params = [
                'llm_override',
                'allowed_tool_ids',
                'forced_tool_id',
                'file_descriptors',
                'search_filters',
                'deep_research',
            ]
            for param in optional_params:
                self.assertNotIn(
                    param, payload, f"Payload should not contain {param}"
                )


class TestStreamingResponseHandling(unittest.TestCase):
    """Test suite for Task Group 2: Response Handling Verification."""

    def setUp(self):
        """Set up test configuration."""
        self.config = Configuration()
        self.config.gpt_server = 'http://test-server'
        self.config.gpt_persona = 1
        self.config._gpt_persona = 1
        self.config.debug = False
        self.config._generate_assistant_api_key = Mock(return_value='test-key')
        self.config.get_new_chat_id = Mock(return_value=123)
        self.config.smooth_print = Mock()
        self.config.clear_console = Mock()

    def test_initial_packet_parsing(self):
        """Test initial packet parsing with message IDs."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 100,
                            'reserved_assistant_message_id': 200,
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            message_id, api_key = self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify message ID was extracted correctly
            self.assertEqual(message_id, 200)
            self.assertEqual(api_key, 'test-key')

    def test_reasoning_events_handling(self):
        """Test reasoning_start and reasoning_delta event handling."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'turn_index': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'step1',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            with patch('vss_cli.config.Spinner') as mock_spinner_cls:
                mock_spinner = MagicMock()
                mock_spinner_cls.return_value = mock_spinner

                self.config.ask_assistant(
                    message='test message',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,
                )

                # Verify spinner was started and stopped
                mock_spinner_cls.assert_called_once()
                mock_spinner.start.assert_called_once()
                mock_spinner.stop.assert_called_once()

    def test_message_events_handling(self):
        """Test message_start and message_delta event handling."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 0,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 1,
                            'obj': {
                                'type': 'message_delta',
                                'content': 'Hello',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 2,
                            'obj': {
                                'type': 'message_delta',
                                'content': ' World',
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify smooth_print was called with message content
            smooth_print_calls = [
                call[0][0] for call in self.config.smooth_print.call_args_list
            ]
            self.assertIn('Hello', smooth_print_calls)
            self.assertIn(' World', smooth_print_calls)

    def test_citation_events_handling(self):
        """Test citation_start and citation_delta event handling."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 0,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {'turn_index': 1, 'obj': {'type': 'citation_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 2,
                            'obj': {
                                'type': 'citation_delta',
                                'citations': [
                                    {'id': 1, 'text': 'citation text'}
                                ],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Should not raise any exceptions
            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

    def test_section_end_and_stop_events_handling(self):
        """Test section_end and stop event handling."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 0,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {'turn_index': 1, 'obj': {'type': 'section_end'}}
                    ).encode(),
                    json.dumps(
                        {'turn_index': 2, 'obj': {'type': 'stop'}}
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Should not raise any exceptions
            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

    def test_legacy_format_fallback(self):
        """Test legacy format fallback (top_documents, answer_piece)."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'top_documents': [
                                {
                                    'document_id': 'doc1',
                                    'semantic_identifier': 'Doc Title',
                                }
                            ]
                        }
                    ).encode(),
                    json.dumps({'answer_piece': 'Legacy answer'}).encode(),
                ]
            )
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify smooth_print was called with legacy answer
            smooth_print_calls = [
                call[0][0] for call in self.config.smooth_print.call_args_list
            ]
            self.assertIn('Legacy answer', smooth_print_calls)


class TestUserExperiencePreservation(unittest.TestCase):
    """Test suite for Task Group 3: User Experience Verification."""

    def setUp(self):
        """Set up test configuration."""
        self.config = Configuration()
        self.config.gpt_server = 'http://test-server'
        self.config.gpt_persona = 1
        self.config._gpt_persona = 1
        self.config.debug = False
        self.config._generate_assistant_api_key = Mock(return_value='test-key')
        self.config.get_new_chat_id = Mock(return_value=123)
        self.config.smooth_print = Mock()
        self.config.clear_console = Mock()

    def test_smooth_print_called_for_streaming_output(self):
        """Test smooth_print() is called for streaming text output."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 0,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 1,
                            'obj': {
                                'type': 'message_delta',
                                'content': 'Streaming',
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Verify smooth_print was called
            self.config.smooth_print.assert_called()

    def test_reasoning_spinner_when_hidden(self):
        """Test reasoning spinner appears when show_reasoning=False."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'turn_index': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'think',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            with patch('vss_cli.config.Spinner') as mock_spinner_cls:
                mock_spinner = MagicMock()
                mock_spinner_cls.return_value = mock_spinner

                self.config.ask_assistant(
                    message='test message',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,
                )

                # Verify spinner lifecycle
                mock_spinner_cls.assert_called_once()
                mock_spinner.start.assert_called_once()
                mock_spinner.stop.assert_called_once()

    def test_document_formatting_with_final_documents(self):
        """Test document and citation formatting with final_documents."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 0,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [
                                    {
                                        'link': 'http://example.com/doc1',
                                        'semantic_identifier': 'Test Document',
                                    }
                                ],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 1,
                            'obj': {
                                'type': 'message_delta',
                                'content': 'Answer',
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Should not raise any exceptions
            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )


class TestErrorHandling(unittest.TestCase):
    """Test suite for Task Group 4: Error Handling and Final Verification."""

    def setUp(self):
        """Set up test configuration."""
        self.config = Configuration()
        self.config.gpt_server = 'http://test-server'
        self.config.gpt_persona = 1
        self.config._gpt_persona = 1
        self.config.debug = False
        self.config._generate_assistant_api_key = Mock(return_value='test-key')
        self.config.get_new_chat_id = Mock(return_value=123)
        self.config.smooth_print = Mock()
        self.config.clear_console = Mock()

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON responses."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            # Include valid initial packet then malformed JSON
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    b'not valid json',  # Malformed JSON
                ]
            )
            mock_post.return_value = mock_response

            # Should raise json.JSONDecodeError
            with self.assertRaises(json.JSONDecodeError):
                self.config.ask_assistant(
                    message='test message',
                    spinner_cls=None,
                    final_message='test',
                )

    def test_empty_response_handling(self):
        """Test handling of empty streaming response."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            # Should not raise any exceptions
            result = self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )

            # Result should be a tuple
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 2)

    def test_internal_search_tool_events_handling(self):
        """Test internal_search_tool_start and delta event handling."""
        with patch('vss_cli.config.requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 0,
                            'obj': {
                                'type': 'internal_search_tool_start',
                                'is_internet_search': True,
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 1,
                            'obj': {
                                'type': 'internal_search_tool_delta',
                                'queries': ['search query'],
                                'documents': [
                                    {
                                        'document_id': 'doc1',
                                        'semantic_identifier': 'D',
                                    }
                                ],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'turn_index': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Should not raise any exceptions
            self.config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
            )


if __name__ == '__main__':
    unittest.main()
