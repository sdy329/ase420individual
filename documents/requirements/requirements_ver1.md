# Requirements

## Recording Time

The application should allow to record time using the following format:

`Command: record DATE FROM TO TASK TAG`
`Example: record today 09:30 10:30 'studied Java' :STUDY`

- Should have flexibility in the date format, allowing both "YYYY/MM/DD" and natural language like "today."
- Should be able to use AM or PM for the FROM and TO time values.

## Querying Time Usage

Should be able to query his time usage with the following commands:

`query today`: Retrieves all activities for the current day.
`query date`: Retrieves all activities for the date provided.
`query 'Java'`: Retrieves all Java-related activities.
`query :STUDY`: Retrieves all activities with the tag :STUDY.

## Programming Language and Database

- The application should be developed using Python.
- SQLite should be used as the database.
