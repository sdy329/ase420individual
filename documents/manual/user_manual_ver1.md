# Time Tracker User Manual

## Table of Contents

- [Time Tracker User Manual](#time-tracker-user-manual)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Usage](#usage)
  - [Features](#features)
    - [record](#record)
    - [query](#query)

## Introduction

Time Tracker is a simple application that allows you to track your time spent on various tasks. It is designed to be simple and easy to use, and is suitable for both personal and professional use.

## Usage

This program is run from the command line. To run any of the commands below, simply start the command line input with

```
python program.py
```

## Features

### record

Records the time spent on a task.

Format: `record <date|today> <start_time> <end_time> <task> <tag>`

- `date` must be in the format `YYYY/MM/DD`
- `time` must be in the format `HH:MM` or `HH:MM:AM/PM`
- `task` must be surrounded by single quotes \' \'
- `tag` must start with :

Examples:

- `python program.py record today 10:00 12:00 'meeting with boss' :MEETING`
- `python program.py record 2020/09/01 10:00 12:00 'Study' :STUDY`
- `python program.py record 2022/04/06 7:00PM 9:00PM 'Take a nap' :SLEEP`

### query

Queries the database for records that match the given criteria.

Format: `query <query>`

- `query` can be a date, a tag, or a task

Examples:

- `python program.py query today`
- `python program.py query :MEETING`
- `python program.py query 'meeting with boss'`
