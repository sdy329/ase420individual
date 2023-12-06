import pytest
from src.databasemanager import DatabaseManager
from src.strategies import QueryByDateStrategy, QueryByTagStrategy, QueryByTaskStrategy, QueryByDateRangeStrategy

@pytest.fixture
def database_manager():
    return DatabaseManager(':memory:')

def test_create_table(database_manager):
    database_manager.create_table()
    assert 'time_records' in database_manager.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()[0]

def test_clear_db(database_manager):
    database_manager.insert_record('2023/12/01', '10:00', '12:00', 'Task 1', ':SAMPLE')
    database_manager.insert_record('2023/12/02', '14:00', '16:00', 'Task 2', ':SAMPLE')

    assert len(database_manager.query_records(QueryByDateStrategy(), '2023/12/01')) == 1
    assert len(database_manager.query_records(QueryByDateStrategy(), '2023/12/02')) == 1

    database_manager.clear_db()

    assert len(database_manager.query_records(QueryByDateStrategy(), '2023/12/01')) == 0
    assert len(database_manager.query_records(QueryByDateStrategy(), '2023/12/02')) == 0

def test_insert_record(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Task 1'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date, start_time, end_time, task, tag)
    records = database_manager.query_records(QueryByDateStrategy(), date)

    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag, duration)

def test_query_records_by_tag(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Task 1'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(QueryByTagStrategy(), tag)
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag, duration)

def test_query_records_by_task(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Task 1'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(QueryByTaskStrategy(), task)
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag, duration)

def test_query_records_by_date(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Task 1'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(QueryByDateStrategy(), date)
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag, duration)

def test_query_records_by_date_range(database_manager):
    date1 = '2023/12/01'
    date2 = '2023/12/02'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Task 1'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date1, start_time, end_time, task, tag)
    database_manager.insert_record(date2, start_time, end_time, task, tag)

    records = database_manager.query_records(QueryByDateRangeStrategy(), date1, date2)
    assert len(records) == 2

def test_get_all_records(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Task 1'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date, start_time, end_time, task, tag)
    
    records = database_manager.get_all_records()
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag, duration)
