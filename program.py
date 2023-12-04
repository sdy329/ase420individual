import argparse
import sqlite3
from datetime import datetime

class QueryStrategy:
    def execute(self, cursor, value):
        pass

class QueryByDateStrategy(QueryStrategy):
    def execute(self, cursor, value):
        cursor.execute('SELECT * FROM time_records WHERE date = ?', (value,))
        return cursor.fetchall()

class QueryByTagStrategy(QueryStrategy):
    def execute(self, cursor, value):
        cursor.execute('SELECT * FROM time_records WHERE tag LIKE ?', ('%' + value + '%',))
        return cursor.fetchall()

class QueryByTaskStrategy(QueryStrategy):
    def execute(self, cursor, value):
        cursor.execute('SELECT * FROM time_records WHERE task LIKE ?', ('%' + value.strip("'") + '%',))
        return cursor.fetchall()

class DatabaseManager:
    DATE_FORMAT = '%Y/%m/%d'
    TABLE_NAME = 'time_records'

    def __init__(self, db_name=None):
        if db_name is None:
            db_name = 'time_tracker.db'

        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                start_time TEXT,
                end_time TEXT,
                task TEXT,
                tag TEXT
            )
        ''')
        self.conn.commit()

    def insert_record(self, date, start_time, end_time, task, tag):
        self.cursor.execute(f'''
            INSERT INTO {self.TABLE_NAME} (date, start_time, end_time, task, tag)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, task, tag))
        self.conn.commit()

    def query_records(self, query, strategy):
        try:
            query_value = datetime.strptime(query, self.DATE_FORMAT).strftime(self.DATE_FORMAT)
            return strategy.execute(self.cursor, query_value)
        except ValueError:
            if query.lower() == 'today':
                today = datetime.now().strftime(self.DATE_FORMAT)
                return strategy.execute(self.cursor, today)
            else:
                return strategy.execute(self.cursor, query)

    def clear_db(self):
        self.cursor.execute(f'DELETE FROM {self.TABLE_NAME}')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

class RecordCommand:
    @staticmethod
    def execute(args, time_tracker):
        date = args.date
        start_time = args.start_time
        end_time = args.end_time
        task = args.task
        tag = args.tag

        if date.lower() == 'today':
            date = datetime.now().strftime(DatabaseManager.DATE_FORMAT)

        time_tracker.db_manager.insert_record(date, start_time, end_time, task, tag)

class QueryCommand:
    @staticmethod
    def execute(args, time_tracker):
        if args.query[0] == ':':
            query_strategy = QueryByTagStrategy()
        else:
            query_strategy = QueryByTaskStrategy()

        records = time_tracker.db_manager.query_records(args.query, query_strategy)

        for record in records:
            print(record)

class CommandExecutor:
    def __init__(self, time_tracker):
        self.time_tracker = time_tracker

    def execute_command(self, args):
        if args.command == 'record':
            RecordCommand.execute(args, self.time_tracker)
        elif args.command == 'query':
            QueryCommand.execute(args, self.time_tracker)
        else:
            print("Invalid command.")

class TimeTrackerCLI:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.command_executor = CommandExecutor(self)

    def run(self, args):
        self.command_executor.execute_command(args)

    def close_connection(self):
        self.db_manager.close_connection()

def parse_args():
    parser = argparse.ArgumentParser(description='Time Tracker CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    record_parser = subparsers.add_parser('record', help='Record time usage')
    record_parser.add_argument('date', help='Date in the format YYYY/MM/DD or "today"')
    record_parser.add_argument('start_time', help='Start time in the format HH:MM')
    record_parser.add_argument('end_time', help='End time in the format HH:MM')
    record_parser.add_argument('task', help='Task description')
    record_parser.add_argument('tag', help='Tag for the activity')

    query_parser = subparsers.add_parser('query', help='Query time usage')
    query_parser.add_argument('query', help='Query string')

    return parser.parse_args()

def main():
    args = parse_args()
    time_tracker = TimeTrackerCLI()
    time_tracker.run(args)
    time_tracker.close_connection()

if __name__ == '__main__':
    main()
