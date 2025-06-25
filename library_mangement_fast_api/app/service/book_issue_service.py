from app.data.file_data import load_json, save_json
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger

ISSUED_FILE = "app/data/issued.json"
BOOKS_FILE = "app/data/books.json"
STUDENTS_FILE = "app/data/students.json"

logger = get_logger(__name__)

@handle_exceptions
def issue_book():
    student_id = input("Enter Student ID: ").strip()
    book_id = input("Enter Book ID: ").strip()

    students = load_json(STUDENTS_FILE)
    books = load_json(BOOKS_FILE)
    issued = load_json(ISSUED_FILE)

    if not any(s["student_id"] == student_id for s in students):
        logger.info(f"Student Id :{student_id}  Not FOund")
        raise ValueError("Student not found.")
    
    book = next((b for b in books if b["book_id"] == book_id), None)
    if not book:
        logger.info(f"book :{book}  Not FOund")
        raise ValueError("Book not found.")

    if book["available_copies"] <= 0:
        logger.info("No available copies of this book")
        raise ValueError("No available copies of this book.")

    if any(entry["student_id"] == student_id and entry["book_id"] == book_id for entry in issued):
        logger.info(f"Book : {book_id} already issued to this student {student_id }.")
        raise ValueError("Book already issued to this student.")

    # Issue book
    issued.append({"student_id": student_id, "book_id": book_id})
    book["available_copies"] -= 1

    save_json(ISSUED_FILE, issued)
    save_json(BOOKS_FILE, books)

    logger.info(f"Issued Book {book_id} to Student {student_id}")
    print(f"Issued Book {book_id} to Student {student_id}")

@handle_exceptions
def return_book():
    student_id = input("Enter Student ID: ").strip()
    book_id = input("Enter Book ID: ").strip()

    issued = load_json(ISSUED_FILE)
    books = load_json(BOOKS_FILE)

    if not any(entry["student_id"] == student_id and entry["book_id"] == book_id for entry in issued):
        raise ValueError("This book was not issued to the student.")

    # Remove from issued list
    updated_issued = [entry for entry in issued if not (entry["student_id"] == student_id and entry["book_id"] == book_id)]

    # Update available copies
    for book in books:
        if book["book_id"] == book_id:
            book["available_copies"] += 1
            break

    save_json(ISSUED_FILE, updated_issued)
    save_json(BOOKS_FILE, books)

    logger.info(f"Returned Book {book_id} from Student {student_id}")
    print(f"Returned Book {book_id} from Student {student_id}")

@handle_exceptions
def view_issued_books():
    issued = load_json(ISSUED_FILE)
    students = load_json(STUDENTS_FILE)
    books = load_json(BOOKS_FILE)

    print("Issued Books:")
    for entry in issued:
        student_name = next((s["name"] for s in students if s["student_id"] == entry["student_id"]), "Unknown")
        book_title = next((b["title"] for b in books if b["book_id"] == entry["book_id"]), "Unknown")
        print(f"Student: {student_name} (ID: {entry['student_id']}), Book: {book_title} (ID: {entry['book_id']})")
