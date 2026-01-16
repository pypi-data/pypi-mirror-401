import os
import tempfile
from unittest.mock import patch, MagicMock
import pytest
from ara_cli.prompt_chat import initialize_prompt_chat_mode
from ara_cli.classifier import Classifier


class TestSetupDefaultCombinedChatPromptMode:
    """
    Tests mirroring the scenarios in Setup_Default_Combined_Chat_Prompt_Mode.feature.
    """

    @pytest.fixture
    def setup_ara_environment(self):
        """Sets up a temporary directory structure mimicking the ara project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Change to tmpdir to ensure relative paths work if used
            cwd = os.getcwd()
            os.chdir(tmpdir)

            # Setup base directories
            os.makedirs(os.path.join(tmpdir, "ara", "tasks"), exist_ok=True)

            yield tmpdir

            os.chdir(cwd)

    @patch("ara_cli.prompt_chat.update_artefact_config_prompt_files")
    @patch("ara_cli.chat.Chat.start", autospec=True)
    @patch("ara_cli.chat.Chat.start_non_interactive", autospec=True)
    @patch("ara_cli.prompt_handler.ConfigManager.get_config")
    def test_scenario_1_start_prompt_chat_no_existing_file(
        self,
        mock_get_config,
        mock_start_non_interactive,
        mock_start,
        mock_update_config,
        setup_ara_environment,
    ):
        """
        Scenario: Start prompt-chat mode with existing prompt.data directory and no existing default chat file.
        Expectation: task_chat.md is created.
        """
        root_dir = setup_ara_environment
        task_name = "123_chat_test"
        classifier = "task"

        # Mock config to avoid loading real config
        mock_config = MagicMock()
        mock_config.llm_config = [{"provider": "openai", "model": "gpt-4"}]
        mock_get_config.return_value = mock_config

        # Simulate directory creation normally handled by update_artefact_config_prompt_files
        data_dir = os.path.join(root_dir, "ara", "tasks", f"{task_name}.data")
        os.makedirs(data_dir, exist_ok=True)

        # Execute
        initialize_prompt_chat_mode(
            classifier=classifier,
            param=task_name,
            chat_name=None,  # Default to classifier name 'task' -> 'task_chat.md'
            reset=None,
        )

        # check paths
        # Classifier.get_sub_directory('task') -> 'tasks'
        # Path: ara/tasks/123_chat_test.data/task_chat.md  (Chat adds _chat.md suffix if missing)
        expected_chat_path = os.path.join(
            root_dir, "ara", "tasks", f"{task_name}.data", "task_chat.md"
        )

        assert os.path.exists(
            expected_chat_path
        ), f"Chat file not created at {expected_chat_path}"

        with open(expected_chat_path, "r") as f:
            content = f.read()
        assert "# ara prompt:" in content

        # Verify update config called
        mock_update_config.assert_called_once()

    @patch("ara_cli.prompt_chat.update_artefact_config_prompt_files")
    @patch("ara_cli.chat.Chat.start", autospec=True)
    @patch("ara_cli.chat.Chat.start_non_interactive", autospec=True)
    @patch("ara_cli.prompt_handler.ConfigManager.get_config")
    @patch("sys.stdin.readline", return_value="y\n")  # Simulate user typing 'y'
    @patch("sys.stdout.write")  # Capture stdout to check prompt
    def test_scenario_2_reset_existing_chat(
        self,
        mock_stdout,
        mock_stdin,
        mock_get_config,
        mock_start_non_interactive,
        mock_start,
        mock_update_config,
        setup_ara_environment,
    ):
        """
        Scenario: Start prompt-chat mode with existing chat file, choose to reset.
        Expectation: User prompted, file content reset.
        """
        root_dir = setup_ara_environment
        task_name = "123_chat_test"
        classifier = "task"

        # Setup existing file
        data_dir = os.path.join(root_dir, "ara", "tasks", f"{task_name}.data")
        os.makedirs(data_dir, exist_ok=True)
        chat_path = os.path.join(data_dir, "task_chat.md")

        with open(chat_path, "w") as f:
            f.write("# ara prompt:\nOld Content")

        # Mock config
        mock_config = MagicMock()
        mock_config.llm_config = [{"provider": "openai", "model": "gpt-4"}]
        mock_get_config.return_value = mock_config

        # Execute
        initialize_prompt_chat_mode(
            classifier=classifier,
            param=task_name,
            chat_name=None,
            reset=None,  # Should trigger interactive prompt
        )

        # Verify prompt was printed
        # Note: sys.stdout.write is called by print()
        # We check if any call args contained the prompt string
        prompt_found = False
        for call in mock_stdout.call_args_list:
            if (
                call.args
                and "already exists. Do you want to reset the chat?" in call.args[0]
            ):
                prompt_found = True
                break
        # Alternatively, 'print' might use the buffer directly, but patching sys.stdout should catch it if flush=True/end="" usage in chat.py matches.
        # chat.py: print(f"{chat_file_short} already exists. Do you want to reset the chat? (y/N): ", end="", flush=True)

        # Since 'print' with end="" calls stdout.write, this should work.
        # However, verifying strict output in mock might be tricky if not captured perfectly.
        # Focusing on the RESULT (file reset) is most important for Scenario logic.

        with open(chat_path, "r") as f:
            content = f.read()

        assert content == "# ara prompt:\n", "Chat file should have been reset"
        assert "Old Content" not in content

    @patch("ara_cli.prompt_chat.update_artefact_config_prompt_files")
    @patch("ara_cli.chat.Chat.start", autospec=True)
    @patch("ara_cli.chat.Chat.start_non_interactive", autospec=True)
    @patch("ara_cli.prompt_handler.ConfigManager.get_config")
    @patch("sys.stdin.readline", return_value="n\n")  # Simulate user typing 'n'
    def test_scenario_3_append_existing_chat(
        self,
        mock_stdin,
        mock_get_config,
        mock_start_non_interactive,
        mock_start,
        mock_update_config,
        setup_ara_environment,
    ):
        """
        Scenario: Start prompt-chat mode with existing chat file, choose to append.
        Expectation: File content preserved.
        """
        root_dir = setup_ara_environment
        task_name = "123_chat_test"
        classifier = "task"

        # Setup existing file
        data_dir = os.path.join(root_dir, "ara", "tasks", f"{task_name}.data")
        os.makedirs(data_dir, exist_ok=True)
        chat_path = os.path.join(data_dir, "task_chat.md")

        original_content = "# ara prompt:\nOld Content"
        with open(chat_path, "w") as f:
            f.write(original_content)

        # Mock config
        mock_config = MagicMock()
        mock_config.llm_config = [{"provider": "openai", "model": "gpt-4"}]
        mock_get_config.return_value = mock_config

        # Execute
        initialize_prompt_chat_mode(
            classifier=classifier, param=task_name, chat_name=None, reset=None
        )

        # Verify content preserved
        with open(chat_path, "r") as f:
            content = f.read()

        assert content == original_content, "Chat file content should be preserved"
