import argparse
from datetime import datetime
from src.databasemanager import DatabaseManager
from src.commands import CommandExecutor

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