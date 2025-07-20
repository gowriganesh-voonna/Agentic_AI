from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from pymongo import MongoClient
import torch
import numpy as np
 
from app.models.schemas import QueryInput, Document
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger
 
# FastAPI Router initialization
router = APIRouter()
 
# Logger initialization
logger = get_logger(__name__)
 
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
 
# Utility function to get embeddings using GPT2 model
def get_embedding(text: str):
    with torch.no_grad():
        inputs = tokenizer.encode(text, return_tensors="pt")
        outputs = model.transformer(inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        logger.info(f"Generated embedding for input text of length {len(text)}")
        return embedding.tolist()
 
# Insert a single document into MongoDB
@handle_exceptions
@router.post("/insert", tags=["MongoDB"])
async def insert_document(doc: Document):
    logger.info(f"Received document for insertion: {doc.title}")
    embedding = get_embedding(doc.content)
    result = docs_collection.insert_one({**doc.dict(), "embedding": embedding})
    if result.inserted_id:
        logger.info(f"Document inserted with ID: {result.inserted_id}")
        return {"message": "Document inserted", "id": str(result.inserted_id)}
    logger.error("Document insertion failed")
    raise HTTPException(status_code=500, detail="Insertion failed")
 
# Insert multiple documents into MongoDB
@handle_exceptions
@router.post("/insert_many", tags=["MongoDB"])
async def insert_many(documents: List[Document]):
    logger.info(f"Inserting {len(documents)} documents")
    docs = []
    for doc in documents:
        docs.append({**doc.dict(), "embedding": get_embedding(doc.content)})
    result = docs_collection.insert_many(docs)
    logger.info(f"Inserted document IDs: {[str(_id) for _id in result.inserted_ids]}")
    return {"message": "Documents inserted", "ids": [str(_id) for _id in result.inserted_ids]}
 
# Search documents in MongoDB by title
@handle_exceptions
@router.get("/search/{title}", tags=["MongoDB"])
async def search_by_title(title: str):
    logger.info(f"Searching for documents with title: {title}")
    docs = list(docs_collection.find({"title": title}, {"_id": 0}))
    if not docs:
        logger.warning(f"No documents found with title: {title}")
        raise HTTPException(status_code=404, detail="No documents found")
    logger.info(f"Found {len(docs)} documents with title: {title}")
    return docs
 
# Count tokens in input query using GPT2 tokenizer
@handle_exceptions
@router.post("/tokenize", tags=["GPT2"])
async def count_tokens(query: QueryInput):
    logger.info(f"Tokenizing input: {query.question}")
    tokens = tokenizer.encode(query.question)
    token_splitting = tokenizer.tokenize(query.question)
    logger.info(f"Token count: {len(tokens)}")
    return {"token_count": len(tokens), "tokens": tokens,"token_names":token_splitting}
 
# Generate text response using GPT2 model
@handle_exceptions
@router.post("/generate", tags=["GPT2"])
async def generate_text(query: QueryInput):
    logger.info(f"Generating response for input: {query.question}")
    inputs = tokenizer.encode(query.question, return_tensors="pt")
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    logger.info(f"Generated response: {response}")
    return {"generated_response": response}
 
# Root health check or base endpoint
@handle_exceptions
@router.get("/", tags=["General"])
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "FastAPI + MongoDB + GPT2 + Embeddings Example"}

 