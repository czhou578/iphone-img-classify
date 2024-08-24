import sqlite3

conn = sqlite3.connect("pictures.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE images (
        id INTEGER PRIMARY KEY,
        path TEXT NOT NULL,
        name TEXT NOT NULL,
        keywords TEXT NOT NULL,
        taken_date TEXT NOT NULL
    );
''')

