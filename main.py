import sqlite3
from datetime import datetime

conn = sqlite3.connect('time_tracker.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS time_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        start_time TEXT,
        end_time TEXT,
        task TEXT,
        tag TEXT
    )
''')
conn.commit()

def record_time(command):
    parts = command.split()
    date = parts[0]
    start_time = parts[1]
    end_time = parts[2]
    task = ' '.join(parts[3:-1])
    tag = parts[-1]

    if date.lower() == 'today':
        date = datetime.now().strftime('%Y/%m/%d')

    cursor.execute('''
        INSERT INTO time_records (date, start_time, end_time, task, tag)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, start_time, end_time, task, tag))
    conn.commit()

def query(command):
    _, query = command.split()

    try:
        datetime.strptime(query, '%Y/%m/%d')
        cursor.execute('SELECT * FROM time_records WHERE date = ?', (query,))
    except ValueError:
        if query.lower() == 'today':
            today = datetime.now().strftime('%Y/%m/%d')
            cursor.execute('SELECT * FROM time_records WHERE date = ?', (today,))

        elif query[0] == ':':
            cursor.execute('SELECT * FROM time_records WHERE tag LIKE ?', ('%' + query + '%',))

        else:
            cursor.execute('SELECT * FROM time_records WHERE task LIKE ?', ('%' + query.strip("'") + '%',))

    records = cursor.fetchall()
    for record in records:
        print(record)

def clear_db():
    cursor.execute('DELETE FROM time_records')
    conn.commit()

record_time("today 09:30AM 10:30AM 'studied Python' :STUDY")
record_time("2023/12/02 12:00PM 1:30PM 'worked on project' :WORK")
print('---')
query("query today")
print('---')
query("query 2023/12/02")
print('---')
query("query 'Python'")
print('---')
query("query :STUDY")
print('---')
clear_db()

conn.close()
