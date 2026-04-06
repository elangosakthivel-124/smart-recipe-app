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
import sqlite3

DB_NAME = "library.db"

def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print("❌ Connection error:", e)
        return None


# ➕ Add Book
def add_book(title, author, publisher, year, isbn, copies):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO books (title, author, publisher, year_published, isbn, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, author, publisher, year, isbn, copies, copies))

        conn.commit()
        print("✅ Book added successfully")

    except sqlite3.IntegrityError:
        print("⚠️ ISBN already exists (must be unique)")
    except sqlite3.Error as e:
        print("❌ Error adding book:", e)
    finally:
        if conn:
            conn.close()


# 📖 View All Books
def view_books():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        if not books:
            print("📭 No books found")
            return

        print("\n📚 Book List:")
        print("-" * 80)

        for book in books:
            print(f"""
ID: {book[0]}
Title: {book[1]}
Author: {book[2]}
Publisher: {book[3]}
Year: {book[4]}
ISBN: {book[5]}
Total Copies: {book[6]}
Available: {book[7]}
""")
        print("-" * 80)

    except sqlite3.Error as e:
        print("❌ Error fetching books:", e)
    finally:
        if conn:
            conn.close()


# 🧪 Test Run
def main():
    print("=== Day 3: Book Management ===")

    # Sample Data (you can change)
    add_book("Python Basics", "John Doe", "ABC Pub", 2022, "ISBN001", 5)
    add_book("Data Structures", "Jane Smith", "XYZ Pub", 2021, "ISBN002", 3)

    view_books()


if __name__ == "__main__":
    main()

import sqlite3

DB_NAME = "library.db"

def create_connection():
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print("❌ Connection error:", e)
        return None


# 🔍 Search by Title
def search_by_title(title):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM books WHERE title LIKE ?
        """, ('%' + title + '%',))

        results = cursor.fetchall()
        display_results(results)

    except sqlite3.Error as e:
        print("❌ Error searching by title:", e)
    finally:
        if conn:
            conn.close()


# 🔍 Search by Author
def search_by_author(author):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM books WHERE author LIKE ?
        """, ('%' + author + '%',))

        results = cursor.fetchall()
        display_results(results)

    except sqlite3.Error as e:
        print("❌ Error searching by author:", e)
    finally:
        if conn:
            conn.close()


# 🔍 Search by ISBN
def search_by_isbn(isbn):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM books WHERE isbn = ?
        """, (isbn,))

        results = cursor.fetchall()
        display_results(results)

    except sqlite3.Error as e:
        print("❌ Error searching by ISBN:", e)
    finally:
        if conn:
            conn.close()


# 📊 Display Function (Reusable)
def display_results(books):
    if not books:
        print("📭 No matching books found")
        return

    print("\n📚 Search Results:")
    print("-" * 80)

    for book in books:
        print(f"""
ID: {book[0]}
Title: {book[1]}
Author: {book[2]}
Publisher: {book[3]}
Year: {book[4]}
ISBN: {book[5]}
Total Copies: {book[6]}
Available: {book[7]}
""")

    print("-" * 80)


# 🧪 Test Run
def main():
    print("=== Day 4: Search & Filter ===")

    # Example searches
    search_by_title("Python")
    search_by_author("Jane")
    search_by_isbn("ISBN001")


if __name__ == "__main__":
    main()
    import sqlite3
from datetime import date

DB_NAME = "library.db"

def create_connection():
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print("❌ Connection error:", e)
        return None


# ➕ Add Member
def add_member(name, email, phone):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        join_date = date.today().isoformat()

        cursor.execute("""
        INSERT INTO members (name, email, phone, join_date)
        VALUES (?, ?, ?, ?)
        """, (name, email, phone, join_date))

        conn.commit()
        print("✅ Member added successfully")

    except sqlite3.IntegrityError:
        print("⚠️ Email already exists (must be unique)")
    except sqlite3.Error as e:
        print("❌ Error adding member:", e)
    finally:
        if conn:
            conn.close()


# 👥 View Members
def view_members():
    try:
        conn = create_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM members")
        members = cursor.fetchall()

        if not members:
            print("📭 No members found")
            return

        print("\n👥 Member List:")
        print("-" * 70)

        for m in members:
            print(f"""
Member ID: {m[0]}
Name: {m[1]}
Email: {m[2]}
Phone: {m[3]}
Join Date: {m[4]}
""")

        print("-" * 70)

    except sqlite3.Error as e:
        print("❌ Error fetching members:", e)
    finally:
        if conn:
            conn.close()


# 🧪 Test Run
def main():
    print("=== Day 5: Member Management ===")

    # Sample Data
    add_member("Elango Sakthivel", "elango@email.com", "9876543210")
    add_member("Arun Kumar", "arun@email.com", "9123456780")

    view_members()


if __name__ == "__main__":
    main()
    import sqlite3
from datetime import date, timedelta

DB_NAME = "library.db"

def create_connection():
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print("❌ Connection error:", e)
        return None


# 📌 Check Book Availability
def get_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()

    conn.close()
    return book


# 📌 Check Member Exists
def get_member(member_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM members WHERE member_id = ?", (member_id,))
    member = cursor.fetchone()

    conn.close()
    return member


# 🔄 Issue Book
def issue_book(book_id, member_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()

        # Validate Book
        book = get_book(book_id)
        if not book:
            print("❌ Book not found")
            return

        if book[7] <= 0:
            print("⚠️ No copies available")
            return

        # Validate Member
        member = get_member(member_id)
        if not member:
            print("❌ Member not found")
            return

        issue_date = date.today()
        due_date = issue_date + timedelta(days=14)

        # Insert issue record
        cursor.execute("""
        INSERT INTO issued_books (book_id, member_id, issue_date, due_date)
        VALUES (?, ?, ?, ?)
        """, (book_id, member_id, issue_date, due_date))

        # Update available copies
        cursor.execute("""
        UPDATE books
        SET available_copies = available_copies - 1
        WHERE book_id = ?
        """, (book_id,))

        conn.commit()
        print("✅ Book issued successfully")
        print(f"📅 Due Date: {due_date}")

    except sqlite3.Error as e:
        print("❌ Error issuing book:", e)
    finally:
        if conn:
            conn.close()


# 🧪 Test Run
def main():
    print("=== Day 6: Issue Book ===")

    # Example (ensure IDs exist in your DB)
    issue_book(1, 1)


if __name__ == "__main__":
    main()
