from pydantic import BaseModel

# Pydantic models
class Document(BaseModel):
    title: str
    content: str
 
class QueryInput(BaseModel):
    question: str