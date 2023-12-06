# Time Tracker CLI Design Document

## 1. Introduction

The Time Tracker CLI is a command-line interface application designed to help users record, query, and generate reports on their time usage. The application allows users to track the time spent on tasks, categorize activities with tags, and retrieve insights into their productivity.

## 2. System Architecture

The system architecture consists of several components, including the CLI interface, command execution, database management, and query strategies.

### 2.1. Components

#### 2.1.1. Main Program (program.py)

- Responsible for parsing command-line arguments.
- Initializes the TimeTrackerCLI and executes the specified command.

#### 2.1.2. Commands (commands.py)

- Defines various commands such as RecordCommand, QueryCommand, ReportCommand, PriorityCommand, and ClearCommand.
- Each command is responsible for executing specific actions, interacting with the database, and providing feedback to the user.

#### 2.1.3. Database Manager (databasemanager.py)

- Manages the SQLite database for storing time records.
- Handles database connection, table creation, record insertion, querying, clearing, and closing the connection.

#### 2.1.4. Query Strategies (strategies.py)

- Defines different strategies for querying the database, such as querying by date, tag, task, and date range.
- Encapsulates the logic for executing specific types of queries.

#### 2.1.5. Time Tracker CLI (timetrackercli.py)

- Represents the main application class.
- Initializes the DatabaseManager and CommandExecutor.
- Responsible for running the CLI, executing commands, and managing the database connection.

### 2.2. Interaction Flow

- The user executes the CLI with a specific command and arguments.
- The main program parses the arguments and initializes the TimeTrackerCLI.
- The TimeTrackerCLI uses the CommandExecutor to execute the specified command.
- The CommandExecutor delegates the command execution to the appropriate command class.
- Command classes interact with the DatabaseManager to perform actions on the SQLite database.
- The DatabaseManager uses query strategies to retrieve data from the database.
- Results are displayed to the user, providing feedback on the executed command.

## 3. Database Schema

The SQLite database has a single table named time_records with the following columns:

id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
date (DATE)
start_time (TEXT)
end_time (TEXT)
task (TEXT)
tag (TEXT)
duration (INTEGER)

## 4. Command Line Interface

The CLI supports the following commands:

- record: Records time usage with date, start time, end time, task, and tag.
- query: Queries time records based on date, tag, or task.
- report: Generates a time usage report for a specified date range.
- priority: Retrieves a priority task list based on tag durations.
- clear: Clears the entire database.
