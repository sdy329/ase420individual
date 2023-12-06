from src.timetrackercli import TimeTrackerCLI, parse_args

if __name__ == '__main__':
    args = parse_args()
    time_tracker = TimeTrackerCLI()
    time_tracker.run(args)
    time_tracker.close_connection()
