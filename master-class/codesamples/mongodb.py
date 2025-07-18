from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os
 
# Load environment variables
load_dotenv()
 
app = FastAPI()
 
# Connect to MongoDB
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.bookstore
 
# Pydantic model for validation
class Book(BaseModel):
    title: str
    author: str
 
# Create a new book
@app.post("/books")
async def create_book(book: Book):
    result = await db.books.insert_one(book.dict())
    return {"message": "Book added", "id": str(result.inserted_id)}
 
# Read all books
@app.get("/books")
async def get_books():
    books = []
    cursor = db.books.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        books.append(document)
    return books
 
# Read book by title
@app.get("/books/{title}")
async def get_book_by_title(title: str):
    book = await db.books.find_one({"title": title})
    if book:
        book["_id"] = str(book["_id"])
        return book
    raise HTTPException(status_code=404, detail="Book not found")
 
# Update book by title
@app.put("/books/{title}")
async def update_book(title: str, book: Book):
    result = await db.books.update_one({"title": title}, {"$set": book.dict()})
    if result.modified_count:
        return {"message": "Book updated"}
    raise HTTPException(status_code=404, detail="Book not found")
 
# Delete book by title
@app.delete("/books/{title}")
async def delete_book(title: str):
    result = await db.books.delete_one({"title": title})
    if result.deleted_count:
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")