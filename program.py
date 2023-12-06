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

class QueryByDateRangeStrategy(QueryStrategy):
    def execute(self, cursor, start_date, end_date):
        cursor.execute('SELECT * FROM time_records WHERE date BETWEEN ? AND ?', (start_date, end_date))
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
                date DATE,
                start_time TEXT,
                end_time TEXT,
                task TEXT,
                tag TEXT,
                duration INTEGER
            )
        ''')
        self.conn.commit()

    def insert_record(self, date, start_time, end_time, task, tag):
        duration = TimeTrackerCLI.calculate_duration(start_time, end_time)
        self.cursor.execute(f'''
            INSERT INTO {self.TABLE_NAME} (date, start_time, end_time, task, tag, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, task, tag, duration))
        self.conn.commit()
        print("Recorded successfully.")

    def query_records(self, strategy, start_date, end_date=None):
        if end_date:
            return strategy.execute(self.cursor, start_date, end_date)
        else:
            try:
                query_value = datetime.strptime(start_date, self.DATE_FORMAT).strftime(self.DATE_FORMAT)
                return strategy.execute(self.cursor, query_value)
            except ValueError:
                if start_date.lower() == 'today':
                    today = datetime.now().strftime(self.DATE_FORMAT)
                    return strategy.execute(self.cursor, today)
                else:
                    return strategy.execute(self.cursor, start_date)

    def clear_db(self):
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.TABLE_NAME}')
        self.create_table()
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
        
    def get_all_records(self):
        self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME}')
        return self.cursor.fetchall()

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
        if args.query.startswith(':'):
            query_strategy = QueryByTagStrategy()
        elif QueryCommand.is_valid_date(args.query):
            query_strategy = QueryByDateStrategy()
        else:
            query_strategy = QueryByTaskStrategy()

        records = time_tracker.db_manager.query_records(query_strategy, args.query)

        if not records:
            print("No records found.")
        else:
            for record in records:
                print(record)

    @staticmethod
    def is_valid_date(date_string):
        try:
            datetime.strptime(date_string, DatabaseManager.DATE_FORMAT)
            return True
        except ValueError:
            return False

class ReportCommand:
    @staticmethod
    def execute(args, time_tracker):
        start_date = args.start_date
        end_date = args.end_date

        records = time_tracker.db_manager.query_records(QueryByDateRangeStrategy(), start_date, end_date)

        if not records:
            print("No records found.")
        else:
            for record in records:
                print(record)

class PriorityCommand:
    @staticmethod
    def execute(args, time_tracker):
        records = time_tracker.db_manager.query_records(QueryByTagStrategy(), '')

        tag_durations = {}
        for record in records:
            tag = record[5]
            duration = record[6]
            if tag in tag_durations:
                tag_durations[tag] += duration
            else:
                tag_durations[tag] = duration

        sorted_tags = sorted(tag_durations.items(), key=lambda x: x[1], reverse=True)

        for tag, total_duration in sorted_tags:
            print(f'Tag: {tag}, Total Duration: {total_duration} minutes')

class ClearCommand:
    @staticmethod
    def execute(args, time_tracker):
        time_tracker.db_manager.clear_db()
        print("Database cleared.")

class CommandExecutor:
    def __init__(self, time_tracker):
        self.time_tracker = time_tracker

    def execute_command(self, args):
        if args.command == 'record':
            return RecordCommand.execute(args, self.time_tracker)
        elif args.command == 'query':
            return QueryCommand.execute(args, self.time_tracker)
        elif args.command == 'report':
            return ReportCommand.execute(args, self.time_tracker)
        elif args.command == 'priority':
            return PriorityCommand.execute(args, self.time_tracker)
        elif args.command == 'clear':
            return ClearCommand.execute(args, self.time_tracker)
        else:
            return "Invalid command."

class TimeTrackerCLI:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.command_executor = CommandExecutor(self)

    def run(self, args):
        self.command_executor.execute_command(args)

    def close_connection(self):
        self.db_manager.close_connection()

    @staticmethod
    def calculate_duration(start_time, end_time):
        start_datetime = datetime.strptime(start_time, '%I:%M%p') if 'AM' in start_time or 'PM' in start_time else datetime.strptime(start_time, '%H:%M')
        end_datetime = datetime.strptime(end_time, '%I:%M%p') if 'AM' in end_time or 'PM' in end_time else datetime.strptime(end_time, '%H:%M')
        return int((end_datetime - start_datetime).total_seconds() / 60)

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

    report_parser = subparsers.add_parser('report', help='Generate time usage report')
    report_parser.add_argument('start_date', help='Start date in the format YYYY/MM/DD')
    report_parser.add_argument('end_date', help='End date in the format YYYY/MM/DD')

    subparsers.add_parser('priority', help='Get priority task list')

    subparsers.add_parser('clear', help='Clear the database')

    return parser.parse_args()

def main():
    args = parse_args()
    time_tracker = TimeTrackerCLI()
    time_tracker.run(args)
    time_tracker.close_connection()

if __name__ == '__main__':
    main()
