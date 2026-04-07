import sqlite3

DB_NAME = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        publisher TEXT,
        year_published INTEGER,
        isbn TEXT UNIQUE,
        total_copies INTEGER NOT NULL,
        available_copies INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        join_date TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        issue_date TEXT,
        due_date TEXT,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES books(book_id),
        FOREIGN KEY (member_id) REFERENCES members(member_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fines (
        fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
        issue_id INTEGER,
        amount REAL,
        paid INTEGER DEFAULT 0,
        FOREIGN KEY (issue_id) REFERENCES issued_books(issue_id)
    );
    """)

    conn.commit()
    conn.close()
