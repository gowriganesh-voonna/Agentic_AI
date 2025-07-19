from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from pymongo import MongoClient
import torch
 
# Initialize FastAPI
app = FastAPI()
 
# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client.chatdb
qa_collection = db.qa_pairs
 
# Load GPT2
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2", output_hidden_states=True)
model.eval()
 
# Pydantic Models
class QAPair(BaseModel):
    question: str
 
# Endpoint to insert Q&A into MongoDB
@app.post("/ask", tags=["Q&A"])
async def ask_question(payload: QAPair):
    # Tokenize input
    inputs = tokenizer(payload.question, return_tensors="pt")
    
    # Generate response
    outputs = model.generate(**inputs, max_length=50)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
 
    # Get hidden states (embeddings)
    with torch.no_grad():
        output_with_hidden = model(**inputs)
        hidden_states = output_with_hidden.hidden_states[-1]  # last layer
        embedding = torch.mean(hidden_states, dim=1).squeeze().tolist()  # sentence-level embedding
 
    # Store in MongoDB
    data = {
        "question": payload.question,
        "answer": answer,
        "tokens": inputs['input_ids'][0].tolist(),
        "embedding": embedding
    }
 
    result = qa_collection.insert_one(data)
    return {
        "message": "Stored successfully",
        "id": str(result.inserted_id),
        "generated_answer": answer
    }
 
# Search questions in MongoDB
@app.get("/search/{query}", tags=["MongoDB"])
async def search_question(query: str):
    results = list(qa_collection.find({"question": {"$regex": query, "$options": "i"}}, {"_id": 0}))
    if not results:
        raise HTTPException(status_code=404, detail="No matching questions found")
    return results
 
# Count tokens
@app.post("/token-count", tags=["Tokens"])
async def count_tokens(payload: QAPair):
    tokens = tokenizer.encode(payload.question)
    return {
        "token_count": len(tokens),
        "tokens": tokens
    }
 
# Root
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to GPT2 + MongoDB + FastAPI Example"}