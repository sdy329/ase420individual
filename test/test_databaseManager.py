import pytest
from unittest.mock import patch
from program import (
    DatabaseManager,
    QueryByDateStrategy,
    TimeTrackerCLI,
    parse_args,
)

@pytest.fixture
def database_manager():
    return DatabaseManager(':memory:')

def test_create_table(database_manager):
    database_manager.create_table()
    assert 'time_records' in database_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[0]

def test_clear_db(database_manager):
    database_manager.insert_record('2023/12/01', '10:00', '12:00', 'Task 1', 'Tag 1')
    database_manager.insert_record('2023/12/02', '14:00', '16:00', 'Task 2', 'Tag 2')

    assert len(database_manager.query_records('2023/12/01', QueryByDateStrategy())) == 1
    assert len(database_manager.query_records('2023/12/02', QueryByDateStrategy())) == 1

    database_manager.clear_db()

    assert len(database_manager.query_records('2023/12/01', QueryByDateStrategy())) == 0
    assert len(database_manager.query_records('2023/12/02', QueryByDateStrategy())) == 0