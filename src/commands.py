from datetime import datetime
from src.databasemanager import DatabaseManager
from src.strategies import QueryByTagStrategy, QueryByDateStrategy, QueryByTaskStrategy, QueryByDateRangeStrategy

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
        elif QueryCommand.is_valid_date(args.query) or args.query.lower() == 'today':
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