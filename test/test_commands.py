import pytest
from unittest.mock import Mock
from program import (
    TimeTrackerCLI,
    RecordCommand,
    QueryCommand,
    ReportCommand,
    PriorityCommand,
    ClearCommand,
)

@pytest.fixture
def time_tracker():
    return TimeTrackerCLI()

def test_record_command_execute(capsys, time_tracker):
    args = Mock(
        command='record',
        date='2023/12/05',
        start_time='10:00',
        end_time='12:00',
        task='Sample Task',
        tag=':SAMPLE',
    )
    RecordCommand.execute(args, time_tracker)
    captured = capsys.readouterr()
    assert "Recorded successfully." in captured.out

def test_query_command_execute(capsys, time_tracker):
    args = Mock(command='query', query=':SAMPLE')
    QueryCommand.execute(args, time_tracker)
    captured = capsys.readouterr()
    assert "No records found." not in captured.out

def test_report_command_execute(capsys, time_tracker):
    args = Mock(command='report', start_date='2023/12/01', end_date='2023/12/05')
    ReportCommand.execute(args, time_tracker)
    captured = capsys.readouterr()
    assert "No records found." not in captured.out

def test_priority_command_execute(capsys, time_tracker):
    args = Mock(command='priority')
    PriorityCommand.execute(args, time_tracker)
    captured = capsys.readouterr()
    assert "Tag:" in captured.out

def test_clear_command_execute(capsys, time_tracker):
    args = Mock(command='clear')
    ClearCommand.execute(args, time_tracker)
    captured = capsys.readouterr()
    assert "Database cleared." in captured.out
