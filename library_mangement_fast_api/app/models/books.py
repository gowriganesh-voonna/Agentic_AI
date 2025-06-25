from pydantic import BaseModel
from typing import Optional

class Books(BaseModel):
    
    book_id: str
    title: str
    author: str
    genre: str
    total_copies: int
    available_copies: int

    available_copies : int


class Update_book(BaseModel):
    book_id: str
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    total_copies: Optional[int] = None