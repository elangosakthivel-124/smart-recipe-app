from datetime import date, timedelta
from database import get_connection

FINE_PER_DAY = 5


# ➕ Add Book
def add_book(title, author, publisher, year, isbn, copies):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO books (title, author, publisher, year_published, isbn, total_copies, available_copies)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, author, publisher, year, isbn, copies, copies))

        conn.commit()
        return "Book added"

    except:
        return "ISBN already exists"
    finally:
        conn.close()


# ➕ Add Member
def add_member(name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO members (name, email, phone, join_date)
        VALUES (?, ?, ?, ?)
        """, (name, email, phone, date.today().isoformat()))

        conn.commit()
        return "Member added"

    except:
        return "Email already exists"
    finally:
        conn.close()


# 🔄 Issue Book
def issue_book(book_id, member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT available_copies FROM books WHERE book_id=?", (book_id,))
    book = cursor.fetchone()

    if not book:
        return "Book not found"

    if book[0] <= 0:
        return "No copies available"

    issue_date = date.today()
    due_date = issue_date + timedelta(days=14)

    cursor.execute("""
    INSERT INTO issued_books (book_id, member_id, issue_date, due_date)
    VALUES (?, ?, ?, ?)
    """, (book_id, member_id, issue_date, due_date))

    cursor.execute("""
    UPDATE books SET available_copies = available_copies - 1
    WHERE book_id = ?
    """, (book_id,))

    conn.commit()
    conn.close()

    return f"Issued. Due: {due_date}"


# 🔁 Return Book + Fine
def return_book(issue_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT book_id, due_date FROM issued_books WHERE issue_id=?", (issue_id,))
    record = cursor.fetchone()

    if not record:
        return "Issue not found"

    book_id, due_date = record

    today = date.today()
    delay = (today - date.fromisoformat(due_date)).days

    fine = max(0, delay * FINE_PER_DAY)

    cursor.execute("""
    UPDATE issued_books SET return_date=? WHERE issue_id=?
    """, (today, issue_id))

    cursor.execute("""
    UPDATE books SET available_copies = available_copies + 1
    WHERE book_id=?
    """, (book_id,))

    if fine > 0:
        cursor.execute("""
        INSERT INTO fines (issue_id, amount) VALUES (?, ?)
        """, (issue_id, fine))

    conn.commit()
    conn.close()

    return f"Returned. Fine: ₹{fine}"
