import sqlite3


def init_db():
    with sqlite3.connect('example.db') as conn:
        cursor = conn.cursor()
        # Create Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
        ''')
        # Create Posts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
        ''')
        conn.commit()