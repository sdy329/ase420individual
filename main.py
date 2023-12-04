import argparse
import sqlite3
from datetime import datetime

class DatabaseManager:
    DATE_FORMAT = '%Y/%m/%d'
    TABLE_NAME = 'time_records'

    def __init__(self, db_name='time_tracker.db'):
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

    def query_records(self, query):
        try:
            datetime.strptime(query, self.DATE_FORMAT)
            self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME} WHERE date = ?', (query,))
        except ValueError:
            if query.lower() == 'today':
                today = datetime.now().strftime(self.DATE_FORMAT)
                self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME} WHERE date = ?', (today,))
            elif query[0] == ':':
                self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME} WHERE tag LIKE ?', ('%' + query + '%',))
            else:
                self.cursor.execute(f'SELECT * FROM {self.TABLE_NAME} WHERE task LIKE ?', ('%' + query.strip("'") + '%',))

        return self.cursor.fetchall()

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
        records = time_tracker.db_manager.query_records(args.query)

        for record in records:
            print(record)

class TimeTrackerCLI:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def run_command(self, command_str, args):
        if command_str == 'record':
            command = RecordCommand()
        elif command_str == 'query':
            command = QueryCommand()
        else:
            print("Invalid command.")
            return

        command.execute(args, self)

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
    time_tracker.run_command(args.command, args)
    time_tracker.db_manager.close_connection()

if __name__ == '__main__':
    main()
