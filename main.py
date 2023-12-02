import sqlite3
from datetime import datetime

class DatabaseManager:
    DATE_FORMAT = '%Y/%m/%d'
    READABLE_DATE_FORMAT = 'YEAR/MONTH/DAY'
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
        try:
            datetime.strptime(date, self.DATE_FORMAT)
        except ValueError:
            print(f"Error: Invalid date format. Please provide a date in the format {self.READABLE_DATE_FORMAT}.")
            return

        self.cursor.execute(f'''
            INSERT INTO {self.TABLE_NAME} (date, start_time, end_time, task, tag)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, start_time, end_time, task, tag))
        self.conn.commit()
        print("Record inserted.")

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
        self.cursor.execute(f'DROP TABLE {self.TABLE_NAME}')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

class RecordCommand:
    @staticmethod
    def execute(args, time_tracker):
        date = args[0]
        start_time = args[1]
        end_time = args[2]
        task = args[3]
        tag = args[4]

        if date.lower() == 'today':
            date = datetime.now().strftime(DatabaseManager.DATE_FORMAT)
        
        time_tracker.db_manager.insert_record(date, start_time, end_time, task, tag)

class QueryCommand:
    @staticmethod
    def execute(args, time_tracker):
        records = time_tracker.db_manager.query_records(args[0])

        for record in records:
            print(record)

class QuitCommand:
    @staticmethod
    def execute(args, time_tracker):
        time_tracker.db_manager.close_connection()
        print("Quitting...")
        exit()

class ClearCommand:
    @staticmethod
    def execute(args, time_tracker):
        time_tracker.db_manager.clear_db()
        print("Database cleared.")

class HelpCommand:
    @staticmethod
    def execute(args, time_tracker):
        print("Commands:")
        print("record <date> <start_time> <end_time> <task> <tag>")
        print("query <date|'today'|':tag'|'task'>")
        print("clear")
        print("help")
        print("quit")

class TimeTrackerCLI:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def run(self):
        print("Welcome to Time Tracker CLI. Enter 'help' for a list of commands.")
        while True:
            user_input = input("Enter a command: ")
            self.parse_input(user_input)

    def parse_input(self, user_input):
        parts = user_input.split()
        if not parts:
            return

        command_str = parts[0]
        args = parts[1:]

        in_quote = False
        current_arg = ""
        parsed_args = []

        for part in args:
            if part.startswith("'") and part.endswith("'"):
                parsed_args.append(part[1:-1])
            elif part.startswith("'"):
                in_quote = True
                current_arg += part[1:]
            elif part.endswith("'"):
                in_quote = False
                current_arg += " " + part[:-1]
                parsed_args.append(current_arg)
                current_arg = ""
            elif in_quote:
                current_arg += " " + part
            else:
                parsed_args.append(part)
        
        if in_quote:
            print("Error: Unmatched quote in input.")
            return
        
        try:
            if command_str == 'record':
                self.run_command(RecordCommand(), parsed_args)
            elif command_str == 'query':
                self.run_command(QueryCommand(), parsed_args)
            elif command_str == 'quit':
                self.run_command(QuitCommand(), parsed_args)
            elif command_str == 'clear':
                self.run_command(ClearCommand(), parsed_args)
            elif command_str == 'help':
                self.run_command(HelpCommand(), parsed_args)
        except IndexError:
            print("Error: Not enough arguments.")
        

    def run_command(self, command, args):
        command.execute(args, self)

if __name__ == '__main__':
    time_tracker = TimeTrackerCLI()
    time_tracker.run()
    time_tracker.db_manager.close_connection()