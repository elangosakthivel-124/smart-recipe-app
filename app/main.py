from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints.recipes import router as recipes_router

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipes_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "Smart Recipe Generator API is running! 🍳"}
import sqlite3

DB_NAME = "library.db"

def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print("❌ Connection error:", e)
        return None


def create_tables(conn):
    try:
        cursor = conn.cursor()

        # Books Table
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

        # Members Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            join_date DATE
        );
        """)

        # Issued Books Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date DATE,
            due_date DATE,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (member_id) REFERENCES members(member_id)
        );
        """)

        # Fines Table
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
        print("✅ All tables created successfully")

    except sqlite3.Error as e:
        print("❌ Error creating tables:", e)


def show_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table';
        """)
        tables = cursor.fetchall()

        print("\n📋 Tables in database:")
        for table in tables:
            print(f" - {table[0]}")

    except sqlite3.Error as e:
        print("❌ Error fetching tables:", e)


def close_connection(conn):
    if conn:
        conn.close()


def main():
    print("=== Day 2: Create Tables ===\n")

    conn = create_connection()

    if conn:
        create_tables(conn)
        show_tables(conn)
        close_connection(conn)
    else:
        print("❌ Database connection failed")


if __name__ == "__main__":
    main()
