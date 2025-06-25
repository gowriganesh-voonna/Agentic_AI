from app.utiles.logger import get_logger
from app.models.books import Books
from app.data.file_data import load_json,save_json
from app.utiles.decoratores import handle_exceptions

from app.utiles.custom_exceptions import BookIDNotFoundError

logger = get_logger(__name__)

FILE_PATH = "app/data/books.json"
books = load_json(FILE_PATH)
@handle_exceptions
def add_book():
    """ Arugments : Books Class 
    add book method will add book to the books.json file .
    if it already created it will print already exist message else it will add book to 
     the books.json file """
    book = Books(
                    book_id=input("Enter the book_id:").strip(),
                    title = input ("Enter the Book Title:").strip(),
                    author = input("Enter the  author :").strip(),
                    genre= input("ENter the Genre:").strip(),
                    total_copies= int(input("Enter the total_copies:")),
                    available_copies=int(input("Enter the avaiable copies."))
                    
                )
    if any(b["book_id"]== book.book_id for b in books):
        logger.info(f"BooK_id : {book.book_id} Already Exists")
        print(f"Book_id :{book.book_id} is already exists.")
        
     
    else:
        books.append(book.dict())
        logger.info(f"Book_id : {book.book_id} Sucessfully Added")
        save_json(FILE_PATH,books)
        print(f"Book_id: {book.book_id} Added Successfully")
    

@handle_exceptions
def update_book():

    """Arugments : class (Update_book)
    update method will update the book and save it into books.json
    booK_id : Is required
    Remaining optional pararmeters based on user requirements."""

    book_id = input("Enter the book_id :").strip()
    found = False
    for b in books:
        
        if b["book_id"]==book_id:
            found = True
            logger.info(f"Book_id : {book_id} Record Found")
            b["title"] =input ("Enter the New  Book Title (or Leave Blank):").strip() or  b["title"]
            b["author"] = input("Enter the  author (or Leave Blank) :").strip() or  b["author"]
            b["genre"] = input("ENter the Genre: (or Leave Blank)").strip() or  b["genre"]
            b["total_copies"]= int(input("Enter the New total_copies (leave blank to skip)") or 0) or b["total_copies"]
            b["available_copies"] = int(input("Enter the avaible copies (leave blank to skip)") or 0) or b["available_copies"]

    if not found:
        print(f"Book_id : {book_id} Not Found")
    else:
        logger.info(f"books data Updated  successfully")       
        save_json(FILE_PATH,books)
        print(f"Book_id : {book_id} updated Successfully")


    


@handle_exceptions
def view_all_books():
    """view all book method will return all books data."""

    logger.info(f"View all books Method is called")
    books_data=[b for b in books]
    print(books_data)

@handle_exceptions
def search_book():
    """Arugments : book_id or title
     this method will display the book based on book_id or title .If book not found
      it will print Details Not Found """
    text = input("Enter the book_id/title/gener/Author : ").strip() or None
    result = list(filter(lambda b: text in b['book_id'] or text in b["title"] or text in b["genre"],books))

    print(result)
    
    
            
   
@handle_exceptions
def delete_book():
    book_id = input("Enter Book ID: ").strip()
    books = load_json(FILE_PATH)

    if not any(book["book_id"] == book_id for book in books):
        raise BookIDNotFoundError(f"Book ID '{book_id}' not found.")

    update_data= [book for book in books if book["book_id"] != book_id]

    logger.info(f"Book_id : {book_id} deleted Successfully")
    save_json(FILE_PATH,update_data)
    print("Book deleted successfully.")


@handle_exceptions
def generate_report():
    for b in books:
        print(f"Title :{b["title"]} - Issued : {(b["total_copies"] - b["available_copies"])}")






