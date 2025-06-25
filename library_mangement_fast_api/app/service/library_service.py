from app.utiles.logger import get_logger
from app.models.books import Books,Update_book,SearchRequest
from app.data.file_data import load_json,save_json
from app.utiles.decoratores import handle_exceptions
from fastapi import APIRouter,HTTPException
from app.utiles.custom_exceptions import BookIDNotFoundError
from typing import List

logger = get_logger(__name__)
router = APIRouter()

FILE_PATH = "app/data/books.json"
books = load_json(FILE_PATH)

@handle_exceptions
@router.post("/add_books")
async def add_book(book:Books):
    """ Arugments : Books Class 
    add book method will add book to the books.json file .
    if it already created it will print already exist message else it will add book to 
     the books.json file """
    
    if any(b["book_id"]== book.book_id for b in books):
        logger.info(f"BooK_id : {book.book_id} Already Exists")
        raise HTTPException(status_code=400, detail="Book already exists.")
        
     
    books.append(book.dict())
    logger.info(f"Book_id : {book.book_id} Sucessfully Added")
    save_json(FILE_PATH,books)
    refresh_books()
    return { "Message":f"Book_id: {book.book_id} Added Successfully"}
    

@handle_exceptions
@router.put("/update_books/{book_id}")
async def update_book(book_id : str,updated_book : Update_book ):

    """Arugments : class (Update_book)
    update method will update the book and save it into books.json
    booK_id : Is required
    Remaining optional pararmeters based on user requirements."""

    
    found = False
    for b in books:
        
        if b["book_id"]==book_id:
            found = True
            logger.info(f"Book_id : {book_id} Record Found")
            b["title"] =updated_book.title or  b["title"]
            b["author"] = updated_book.author or  b["author"]
            b["genre"] = updated_book.genre or  b["genre"]
            b["total_copies"]= updated_book.total_copies or b["total_copies"]
            b["available_copies"] = updated_book.total_copies or b["available_copies"]

    if not found:
        raise HTTPException(status_code=404,
                            detail=f"Book_id : {book_id} Not Found")
    logger.info(f"books data Updated  successfully")       
    save_json(FILE_PATH,books)
    refresh_books()
    return {"Message": f"Book_id : {book_id} updated Successfully"}
        


    


@handle_exceptions
@router.get("/view_all_books",response_model=List[Books])
async def view_all_books():
    """view all book method will return all books data."""

    logger.info(f"View all books Method is called")
    books_data=[b for b in books]
    return books_data

@handle_exceptions
@router.post("/search_book",response_model=List[Books])
def search_book(request : SearchRequest):
    """Arugments : book_id or title
     this method will display the book based on book_id or title .If book not found
      it will print Details Not Found """
    text = request.query.lower() or None
    result = list(filter(lambda b: text in b['book_id'].lower() or text in b["title"].lower() or text in b["genre"].lower(),books))

    if not result:
        raise HTTPException(status_code=404, detail="No matching books found.")
    logger.info(f"Search query '{text}' found {len(result)} results.")
    return result
    
    
            
   
@handle_exceptions
@router.delete("/delete/{book_id}")
async def delete_book(book_id: str):
    
    global books 

    if not any(book["book_id"] == book_id for book in books):
        raise BookIDNotFoundError(f"Book ID '{book_id}' not found.")

    update_data= [book for book in books if book["book_id"] != book_id]

    logger.info(f"Book_id : {book_id} deleted Successfully")
    save_json(FILE_PATH,update_data)
    refresh_books()
    return {"Message":"Book deleted successfully."}


@handle_exceptions
@router.get("/generate_report",response_model=List)
def generate_report():
    report = []
    for b in books:
        
        report.append({"Title":b["title"],
             "Issued":(b["total_copies"] - b["available_copies"])
             })
    logger.info("Generated book issue report.")
    
    return report



def refresh_books():
    global books
    books = load_json(FILE_PATH)





