import pytest
from unittest.mock import Mock, patch
from program import (
    DatabaseManager,
    CommandExecutor,
    TimeTrackerCLI,
    parse_args,
)


def test_command_executor_invalid_command(capsys):
    command_executor = CommandExecutor(TimeTrackerCLI())
    args = Mock(command='invalid_command')
    result = command_executor.execute_command(args)
    assert result == "Invalid command."

def test_time_tracker_cli_run():
    time_tracker = TimeTrackerCLI()
    with patch.object(CommandExecutor, 'execute_command') as mock_execute_command:
        args = Mock(command='record')
        time_tracker.run(args)
        mock_execute_command.assert_called_once_with(args)

def test_time_tracker_cli_close_connection():
    time_tracker = TimeTrackerCLI()
    with patch.object(DatabaseManager, 'close_connection') as mock_close_connection:
        time_tracker.close_connection()
        mock_close_connection.assert_called_once()
