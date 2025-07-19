from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from pymongo import MongoClient
import torch
import numpy as np
 
# FastAPI app initialization
app = FastAPI()
 
# MongoDB connection using MongoClient
MONGO_URI = "mongodb+srv://gowriganeshvoonna:3EhpwdUK0FnSh3YP@resume-data.wz0y1el.mongodb.net/"
DB_Name = "master-class"
COLLECTION_NAME = "article"
client = MongoClient(MONGO_URI)
db = client[DB_Name]
docs_collection = db[COLLECTION_NAME]
 
# Load GPT2 tokenizer and model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()
 
# Pydantic models
class Document(BaseModel):
    title: str
    content: str
 
class QueryInput(BaseModel):
    question: str
 
# Utility function to get embeddings
def get_embedding(text: str):
    with torch.no_grad():
        inputs = tokenizer.encode(text, return_tensors="pt")
        outputs = model.transformer(inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        return embedding.tolist()
 
# Insert a single document
@app.post("/insert", tags=["MongoDB"])
async def insert_document(doc: Document):
    embedding = get_embedding(doc.content)
    result = docs_collection.insert_one({
        **doc.dict(),
        "embedding": embedding
    })
    if result.inserted_id:
        return {"message": "Document inserted", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Insertion failed")
 
# Insert multiple documents
@app.post("/insert_many", tags=["MongoDB"])
async def insert_many(documents: List[Document]):
    docs = []
    for doc in documents:
        docs.append({**doc.dict(), "embedding": get_embedding(doc.content)})
    result = docs_collection.insert_many(docs)
    return {"message": "Documents inserted", "ids": [str(_id) for _id in result.inserted_ids]}
 
# Search by title
@app.get("/search/{title}", tags=["MongoDB"])
async def search_by_title(title: str):
    docs = list(docs_collection.find({"title": title}, {"_id": 0}))
    if not docs:
        raise HTTPException(status_code=404, detail="No documents found")
    return docs
 
# Token Count API
@app.post("/tokenize", tags=["GPT2"])
async def count_tokens(query: QueryInput):
    tokens = tokenizer.encode(query.question)
    return {"token_count": len(tokens), "tokens": tokens}
 
# Text generation from GPT2
@app.post("/generate", tags=["GPT2"])
async def generate_text(query: QueryInput):
    inputs = tokenizer.encode(query.question, return_tensors="pt")
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_response": response}
 
# Root endpoint
@app.get("/", tags=["General"])
async def root():
    return {"message": "FastAPI + MongoDB + GPT2 + Embeddings Example"}
 