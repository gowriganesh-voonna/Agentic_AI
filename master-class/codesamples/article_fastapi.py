from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
 
app = FastAPI()
 
# Sample in-memory storage
fake_db = {}
 
# Pydantic model
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
 
# ✅ Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}
 
# ✅ GET item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = fake_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item": item}
 
# ✅ GET with query parameter
@app.get("/search/")
def search_item(q: Optional[str] = None):
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    return {"query": q}
 
# ✅ POST to create new item
@app.post("/items/")
def create_item(item: Item):
    item_id = len(fake_db) + 1
    fake_db[item_id] = item.dict()
    return {"message": "Item created", "item_id": item_id, "item": item}
 
# ✅ PUT to update item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found for update")
    fake_db[item_id] = item.dict()
    return {"message": "Item updated", "item_id": item_id, "item": item}
 
# ✅ DELETE item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found for deletion")
    deleted = fake_db.pop(item_id)
    return {"message": "Item deleted", "item": deleted}
 