"""Tests for the assist command --show-reasoning flag."""
import json
import unittest
from unittest.mock import MagicMock, Mock, patch

from click.testing import CliRunner

import vss_cli.cli as cli
from vss_cli.config import Configuration


class TestAssistShowReasoningFlag(unittest.TestCase):
    """Test suite for --show-reasoning flag in assist command."""

    @classmethod
    def setUpClass(cls):
        """Set up test runner."""
        super().setUpClass()
        cls.runner = CliRunner()

    def test_flag_absent_defaults_to_false(self):
        """Test that without --show-reasoning flag, reasoning is hidden (default behavior)."""
        with patch('vss_cli.config.Configuration.ask_assistant') as mock_ask:
            # Mock the ask_assistant method to return dummy values
            mock_ask.return_value = (None, None)

            # Run assist command without --show-reasoning flag
            result = self.runner.invoke(
                cli.cli,
                ['assist', '--no-load', '--no-feedback', 'test question'],
                catch_exceptions=False,
            )

            # Verify command executed
            self.assertEqual(result.exit_code, 0)

            # Verify ask_assistant was called with show_reasoning=False (default)
            mock_ask.assert_called_once()
            call_kwargs = mock_ask.call_args[1]
            self.assertEqual(call_kwargs.get('show_reasoning', False), False)

    def test_flag_present_sets_to_true(self):
        """Test that --show-reasoning flag enables reasoning display."""
        with patch('vss_cli.config.Configuration.ask_assistant') as mock_ask:
            # Mock the ask_assistant method to return dummy values
            mock_ask.return_value = (None, None)

            # Run assist command with --show-reasoning flag
            result = self.runner.invoke(
                cli.cli,
                [
                    'assist',
                    '--no-load',
                    '--no-feedback',
                    '--show-reasoning',
                    'test question',
                ],
                catch_exceptions=False,
            )

            # Verify command executed
            self.assertEqual(result.exit_code, 0)

            # Verify ask_assistant was called with show_reasoning=True
            mock_ask.assert_called_once()
            call_kwargs = mock_ask.call_args[1]
            self.assertEqual(call_kwargs.get('show_reasoning', False), True)

    def test_debug_mode_override(self):
        """Test that debug mode forces reasoning display regardless of flag."""
        with patch('vss_cli.config.Configuration.ask_assistant') as mock_ask:
            # Mock the ask_assistant method to return dummy values
            mock_ask.return_value = (None, None)

            # Run assist command with --debug flag (but without --show-reasoning)
            result = self.runner.invoke(
                cli.cli,
                [
                    '--debug',
                    'assist',
                    '--no-load',
                    '--no-feedback',
                    'test question',
                ],
                catch_exceptions=False,
            )

            # Verify command executed
            self.assertEqual(result.exit_code, 0)

            # Verify ask_assistant was called
            mock_ask.assert_called_once()
            # Debug mode override is checked within ask_assistant method itself
            # This test verifies the CLI layer passes through correctly

    def test_flag_recognized_by_click(self):
        """Test that Click recognizes --show-reasoning as a valid option."""
        # This test verifies the flag is properly registered
        result = self.runner.invoke(
            cli.cli,
            ['assist', '--help'],
            catch_exceptions=False,
        )

        # Verify help text includes the new flag
        self.assertEqual(result.exit_code, 0)
        self.assertIn('--show-reasoning', result.output)
        self.assertIn('display AI reasoning process', result.output)


class TestAskAssistantAPILayer(unittest.TestCase):
    """Test suite for ask_assistant method API layer parameter handling."""

    def test_ask_assistant_accepts_show_reasoning_parameter(self):
        """Test that ask_assistant method accepts show_reasoning parameter."""
        # Create a real Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post at module level
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock the streaming response
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            # Call ask_assistant with show_reasoning parameter
            result = config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
                show_reasoning=True,
            )

            # Verify method accepts the parameter without error
            # The method should complete and return a tuple
            self.assertIsNotNone(result)

    def test_ask_assistant_passes_show_reasoning_to_get_new_chat_id(self):
        """Test that show_reasoning parameter is passed to get_new_chat_id."""
        # Create a real Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post at module level
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock the streaming response
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            # Call ask_assistant with show_reasoning=True
            config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
                show_reasoning=True,
            )

            # Verify get_new_chat_id was called with show_reasoning parameter
            config.get_new_chat_id.assert_called_once()
            call_kwargs = config.get_new_chat_id.call_args[1]
            self.assertEqual(call_kwargs.get('show_reasoning'), True)

    def test_ask_assistant_defaults_show_reasoning_to_false(self):
        """Test that show_reasoning defaults to False when not provided."""
        # Create a real Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post at module level
        with patch('vss_cli.config.requests.post') as mock_post:
            # Mock the streaming response
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_response.iter_lines = Mock(return_value=[])
            mock_post.return_value = mock_response

            # Call ask_assistant WITHOUT show_reasoning parameter (test backward compatibility)
            config.ask_assistant(
                message='test message', spinner_cls=None, final_message='test'
            )

            # Verify get_new_chat_id was called with show_reasoning defaulted to False
            config.get_new_chat_id.assert_called_once()
            call_kwargs = config.get_new_chat_id.call_args[1]
            # Should be False (default value)
            self.assertEqual(call_kwargs.get('show_reasoning'), False)


class TestReasoningDisplayLogic(unittest.TestCase):
    """Test suite for reasoning display logic and spinner behavior."""

    def test_spinner_shows_when_reasoning_hidden(self):
        """Test that spinner displays when reasoning is hidden (show_reasoning=False)."""
        # Create a Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post to simulate streaming with reasoning events
        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate streaming response with reasoning events
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)

            # Simulate event stream: reasoning_start -> reasoning_delta -> message_start
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'thinking...',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Mock Spinner class
            with patch('vss_cli.config.Spinner') as mock_spinner_cls:
                mock_spinner_instance = MagicMock()
                mock_spinner_cls.return_value = mock_spinner_instance

                # Call ask_assistant with show_reasoning=False (default)
                config.ask_assistant(
                    message='test message',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,
                )

                # Verify spinner was created and started
                mock_spinner_cls.assert_called_once()
                mock_spinner_instance.start.assert_called_once()
                # Verify spinner was stopped when message content started
                mock_spinner_instance.stop.assert_called_once()

    def test_reasoning_streams_when_flag_true(self):
        """Test that reasoning is displayed when show_reasoning=True."""
        # Create a Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post to simulate streaming with reasoning events
        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate streaming response with reasoning events
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)

            # Simulate event stream with reasoning delta
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'thinking step 1',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'thinking step 2',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 3,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Call ask_assistant with show_reasoning=True
            config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
                show_reasoning=True,
            )

            # Verify smooth_print was called with reasoning chunks
            smooth_print_calls = [
                call[0][0] for call in config.smooth_print.call_args_list
            ]
            self.assertIn('thinking step 1', smooth_print_calls)
            self.assertIn('thinking step 2', smooth_print_calls)

    def test_debug_mode_forces_reasoning_display(self):
        """Test that debug mode forces reasoning display regardless of show_reasoning flag."""
        # Create a Configuration instance with debug=True
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = True  # Debug mode enabled

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post to simulate streaming with reasoning events
        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate streaming response with reasoning events
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)

            # Simulate event stream with reasoning delta
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'debug reasoning',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Call ask_assistant with show_reasoning=False BUT debug=True
            config.ask_assistant(
                message='test message',
                spinner_cls=None,
                final_message='test',
                show_reasoning=False,  # Flag is false but debug should override
            )

            # Verify smooth_print was called with reasoning (debug override)
            smooth_print_calls = [
                call[0][0] for call in config.smooth_print.call_args_list
            ]
            self.assertIn('debug reasoning', smooth_print_calls)

    def test_reasoning_text_logged_in_all_cases(self):
        """Test that reasoning text is always logged to debug logs."""
        # Create a Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post to simulate streaming with reasoning events
        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate streaming response with reasoning events
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)

            # Simulate event stream with reasoning delta
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'logged reasoning',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Mock the logger
            with patch('vss_cli.config._LOGGING.debug') as mock_log:
                # Call ask_assistant with show_reasoning=False (reasoning hidden)
                config.ask_assistant(
                    message='test message',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,
                )

                # Verify debug logging was called with reasoning text
                log_calls = [str(call) for call in mock_log.call_args_list]
                # Check if any log call contains the reasoning text
                reasoning_logged = any(
                    'logged reasoning' in str(call) for call in log_calls
                )
                self.assertTrue(
                    reasoning_logged,
                    "Reasoning text should be logged to debug logs",
                )

    def test_spinner_lifecycle_start_stop(self):
        """Test spinner lifecycle: starts on reasoning_start, stops on message_start."""
        # Create a Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Mock requests.post to simulate streaming with reasoning events
        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate streaming response with reasoning events
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)

            # Simulate event stream: reasoning_start -> multiple deltas -> message_start
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'step 1',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'step 2',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 3,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'step 3',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 4,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            # Mock Spinner class
            with patch('vss_cli.config.Spinner') as mock_spinner_cls:
                mock_spinner_instance = MagicMock()
                mock_spinner_cls.return_value = mock_spinner_instance

                # Call ask_assistant with show_reasoning=False
                config.ask_assistant(
                    message='test message',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,
                )

                # Verify spinner lifecycle
                # 1. Spinner created on reasoning_start
                mock_spinner_cls.assert_called_once()
                # 2. Spinner started
                mock_spinner_instance.start.assert_called_once()
                # 3. Spinner stopped on message_start
                mock_spinner_instance.stop.assert_called_once()


class TestAssistIntegration(unittest.TestCase):
    """Integration tests for end-to-end --show-reasoning functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test runner."""
        super().setUpClass()
        cls.runner = CliRunner()

    def test_end_to_end_flag_propagation_with_reasoning_hidden(self):
        """Test complete workflow: CLI flag=False -> API -> Display (spinner shown)."""
        # Create a Configuration instance to capture the complete flow
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        # Track whether spinner was created and used correctly
        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate complete streaming response
            mock_response = MagicMock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)

            # Complete event sequence
            mock_response.iter_lines = Mock(
                return_value=[
                    json.dumps(
                        {
                            'user_message_id': 1,
                            'reserved_assistant_message_id': 2,
                        }
                    ).encode(),
                    json.dumps(
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'thinking...',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 3,
                            'obj': {
                                'type': 'message_delta',
                                'content': 'Answer text',
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            with patch('vss_cli.config.Spinner') as mock_spinner_cls:
                mock_spinner = MagicMock()
                mock_spinner_cls.return_value = mock_spinner

                # Call with show_reasoning=False (default)
                result = config.ask_assistant(
                    message='test question',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,
                )

                # Verify complete flow
                # 1. Spinner was created when reasoning started
                mock_spinner_cls.assert_called_once()
                # 2. Spinner was started
                mock_spinner.start.assert_called_once()
                # 3. Reasoning was NOT displayed (smooth_print not called with reasoning)
                smooth_print_calls = [
                    call[0][0] for call in config.smooth_print.call_args_list
                ]
                self.assertNotIn('thinking...', smooth_print_calls)
                # 4. Spinner was stopped when message started
                mock_spinner.stop.assert_called_once()
                # 5. Message content WAS displayed
                self.assertIn('Answer text', smooth_print_calls)

    def test_end_to_end_flag_propagation_with_reasoning_shown(self):
        """Test complete workflow: CLI flag=True -> API -> Display (reasoning shown)."""
        # Create a Configuration instance
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = False

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

        with patch('vss_cli.config.requests.post') as mock_post:
            # Simulate complete streaming response
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
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'analyzing...',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
                            'obj': {
                                'type': 'message_start',
                                'final_documents': [],
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 3,
                            'obj': {
                                'type': 'message_delta',
                                'content': 'Final answer',
                            },
                        }
                    ).encode(),
                ]
            )
            mock_post.return_value = mock_response

            with patch('vss_cli.config.Spinner') as mock_spinner_cls:
                # Call with show_reasoning=True
                result = config.ask_assistant(
                    message='test question',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=True,
                )

                # Verify complete flow
                # 1. NO spinner should be created when reasoning is shown
                mock_spinner_cls.assert_not_called()
                # 2. Reasoning WAS displayed
                smooth_print_calls = [
                    call[0][0] for call in config.smooth_print.call_args_list
                ]
                self.assertIn('analyzing...', smooth_print_calls)
                # 3. Message content also displayed
                self.assertIn('Final answer', smooth_print_calls)

    def test_multiple_flags_interaction_show_reasoning_and_no_feedback(self):
        """Test that --show-reasoning and --no-feedback work together correctly."""
        with patch('vss_cli.config.Configuration.ask_assistant') as mock_ask:
            mock_ask.return_value = (None, None)

            # Run with both flags
            result = self.runner.invoke(
                cli.cli,
                [
                    'assist',
                    '--no-load',
                    '--show-reasoning',
                    '--no-feedback',
                    'test question',
                ],
                catch_exceptions=False,
            )

            # Verify both flags were respected
            self.assertEqual(result.exit_code, 0)
            # show_reasoning=True was passed
            call_kwargs = mock_ask.call_args[1]
            self.assertEqual(call_kwargs.get('show_reasoning'), True)
            # No feedback prompt should appear in output (tested by --no-feedback)
            self.assertNotIn('Rate this response', result.output)

    def test_backward_compatibility_no_flag_provided(self):
        """Test that existing commands without --show-reasoning flag still work (backward compatibility)."""
        with patch('vss_cli.config.Configuration.ask_assistant') as mock_ask:
            mock_ask.return_value = (None, None)

            # Run command WITHOUT the new flag (as users would have done before)
            result = self.runner.invoke(
                cli.cli,
                ['assist', '--no-load', '--no-feedback', 'legacy question'],
                catch_exceptions=False,
            )

            # Verify command still works
            self.assertEqual(result.exit_code, 0)
            # Default behavior should be show_reasoning=False
            mock_ask.assert_called_once()
            call_kwargs = mock_ask.call_args[1]
            self.assertEqual(call_kwargs.get('show_reasoning', False), False)

    def test_debug_mode_overrides_flag_in_complete_workflow(self):
        """Test that debug mode forces reasoning display in complete end-to-end flow."""
        # Create Configuration with debug=True
        config = Configuration()
        config.gpt_server = 'http://test-server'
        config.gpt_persona = 1
        config._gpt_persona = 1
        config.debug = True  # Debug mode ON

        # Mock instance methods
        config._generate_assistant_api_key = Mock(return_value='test-key')
        config.get_new_chat_id = Mock(return_value=123)
        config.smooth_print = Mock()
        config.clear_console = Mock()

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
                        {'ind': 0, 'obj': {'type': 'reasoning_start'}}
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 1,
                            'obj': {
                                'type': 'reasoning_delta',
                                'reasoning': 'debug reasoning chunk',
                            },
                        }
                    ).encode(),
                    json.dumps(
                        {
                            'ind': 2,
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
                # Call with show_reasoning=False BUT debug=True
                result = config.ask_assistant(
                    message='test question',
                    spinner_cls=None,
                    final_message='test',
                    show_reasoning=False,  # Flag says hide, but debug should override
                )

                # Verify debug override worked
                # 1. NO spinner should be created (debug mode shows reasoning)
                mock_spinner_cls.assert_not_called()
                # 2. Reasoning WAS displayed despite show_reasoning=False
                smooth_print_calls = [
                    call[0][0] for call in config.smooth_print.call_args_list
                ]
                self.assertIn('debug reasoning chunk', smooth_print_calls)


if __name__ == '__main__':
    unittest.main()
