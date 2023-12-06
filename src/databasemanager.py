import sqlite3
from datetime import datetime

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
        from src.timetrackercli import TimeTrackerCLI
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
