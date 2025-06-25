from app.data.file_data import load_json, save_json
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger
from fastapi import APIRouter,HTTPException
from typing import List
from app.models.issue_books import IssueBook,ReturnBook

ISSUED_FILE = "app/data/issued.json"
BOOKS_FILE = "app/data/books.json"
STUDENTS_FILE = "app/data/students.json"

logger = get_logger(__name__)
router = APIRouter()

students = load_json(STUDENTS_FILE)
books = load_json(BOOKS_FILE)
issued = load_json(ISSUED_FILE)

@handle_exceptions
@router.post("/books/issue_books")
async def issue_book(data : IssueBook):
    refresh_books()
    refresh_issue_books()
    student_id = data.student_id.strip()
    book_id = data.book_id.strip()


    if not any(s["student_id"] == student_id for s in students):
        logger.info(f"Student Id :{student_id}  Not FOund")
        raise HTTPException(status_code=404,
                            detail="Student not found.")
    
    book = next((b for b in books if b["book_id"] == book_id), None)
    if not book:
        logger.info(f"book :{book}  Not FOund")
        raise HTTPException(status_code=404,
                            detail= "Book not found.")

    if book["available_copies"] <= 0:
        logger.info("No available copies of this book")
        raise HTTPException(status_code=422,
                            detail="No available copies of this book.")           #422 Unprocessable Entity

    if any(entry["student_id"] == student_id and entry["book_id"] == book_id for entry in issued):
        logger.info(f"Book : {book_id} already issued to this student {student_id }.")
        raise HTTPException(status_code=409,
                            detail="Book already issued to this student.")               #409 Conflict

    # Issue book
    issued.append({"student_id": student_id, "book_id": book_id})
    book["available_copies"] -= 1

    save_json(ISSUED_FILE, issued)
    save_json(BOOKS_FILE, books)
    refresh_books()
    refresh_issue_books()

    logger.info(f"Issued Book {book_id} to Student {student_id}")
    return {"Message":f"Issued Book {book_id} to Student {student_id}"}




@handle_exceptions
@router.put("/books/return_books")
async def return_book(data : ReturnBook):
    student_id = data.student_id.strip()
    book_id = data.book_id.strip()

   

    if not any(entry["student_id"] == student_id and entry["book_id"] == book_id for entry in issued):
        raise HTTPException(status_code=404,
                            detail="This book was not issued to the student.")

    # Remove from issued list
    updated_issued = [entry for entry in issued if not (entry["student_id"] == student_id and entry["book_id"] == book_id)]

    # Update available copies
    for book in books:
        if book["book_id"] == book_id:
            book["available_copies"] += 1
            break

    save_json(ISSUED_FILE, updated_issued)
    save_json(BOOKS_FILE, books)
    refresh_books()
    refresh_issue_books()

    logger.info(f"Returned Book {book_id} from Student {student_id}")
    return {"Message":f"Returned Book {book_id} from Student {student_id}"}


@handle_exceptions
@router.get("/books/issued_books",response_model=list)
async def view_issued_books():
    issued_books = []
    for entry in issued:
        student_name = next((s["name"] for s in students if s["student_id"] == entry["student_id"]), "Unknown")
        book_title = next((b["title"] for b in books if b["book_id"] == entry["book_id"]), "Unknown")
        
        issued_books.append({
            "Student_Name": student_name ,
            "Student_ID" : entry['student_id'],
            "Book" : book_title,
            "Book_ID" : entry['book_id']
        })

    return issued_books



def refresh_books():
    global books
    books = load_json(BOOKS_FILE)

def refresh_issue_books():
    global issued
    issued = load_json(ISSUED_FILE)