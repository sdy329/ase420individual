import pytest
from test.test_databaseManager import database_manager
from program import (
    QueryByDateStrategy,
    QueryByTagStrategy,
    QueryByTaskStrategy,
)

def test_query_records_by_tag(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Sample Task'
    tag = 'Sample Tag'

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(tag, QueryByTagStrategy())
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag)

def test_query_records_by_task(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Sample Task'
    tag = 'Sample Tag'

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(task, QueryByTaskStrategy())
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag)

def test_query_records_by_date(database_manager):
    date = '2023/12/01'
    start_time = '10:00'
    end_time = '12:00'
    task = 'Sample Task'
    tag = 'Sample Tag'

    database_manager.insert_record(date, start_time, end_time, task, tag)

    records = database_manager.query_records(date, QueryByDateStrategy())
    assert len(records) == 1
    assert records[0][1:] == (date, start_time, end_time, task, tag)