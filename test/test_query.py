import pytest
from test.test_databaseManager import database_manager
from program import (
    QueryByDateStrategy,
    QueryByTagStrategy,
    QueryByTaskStrategy,
    QueryByDateRangeStrategy,
)

def test_query_records_by_tag(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Sample Task'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(QueryByTagStrategy(),tag)
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag, duration)

def test_query_records_by_task(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Sample Task'
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
    task = 'Sample Task'
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
    task = 'Sample Task'
    tag = ':SAMPLE'
    duration = 120

    database_manager.insert_record(date1, start_time, end_time, task, tag)
    database_manager.insert_record(date2, start_time, end_time, task, tag)

    records = database_manager.query_records(QueryByDateRangeStrategy(), date1, date2)
    assert len(records) == 2
    assert records[0][1:] == (date1, start_time, end_time, task, tag, duration)
    assert records[1][1:] == (date2, start_time, end_time, task, tag, duration)