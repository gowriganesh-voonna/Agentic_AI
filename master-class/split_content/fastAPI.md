
### 1. GET Endpoint
**✅ Description**:
Used to retrieve data.
 
Enter the URL: http://127.0.0.1:8000/
 
Click Send
 
You’ll get the response:
 
```json

{
  "message": "Hello World"
}
```
✅ Now you’ve successfully tested your first FastAPI endpoint!
 
----

### 2. GET Endpoint with Path Parameter
**✅ Description**:
Used to retrieve a specific item by its ID or name.
 
🔧 Code:
```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```
🔗 URL:
Copy code
GET http://127.0.0.1:8000/items/5
🔁 Sample Response:
```json
{
  "item_id": 5
}
```
----

### 3. GET with Query Parameters
**✅ Description**:
Retrieve data using parameters in the URL query string.
 
🔧 Code:
```python
@app.get("/search/")
def search_items(q: str = None):
    return {"query": q}
```
🔗 URL:
GET http://127.0.0.1:8000/search/?q=books
🔁 Sample Response:
```json
{
  "query": "books"
}
```
---

### 4. POST Endpoint
**✅ Description**:
Used to create new data.
 
```Code:
from pydantic import BaseModel
 
class Item(BaseModel):
    name: str
    price: float
 
@app.post("/items/")
def create_item(item: Item):
    return {"item_created": item}
```

🔗 URL:

POST http://127.0.0.1:8000/items/
📨 Sample Request Body (Postman - Body → raw → JSON):

```json

{
  "name": "Laptop",
  "price": 75000
}
```

🔁 Sample Response:
```json
{
  "item_created": {
    "name": "Laptop",
    "price": 75000
  }
}
```
----

### 5. PUT Endpoint
**✅ Description**:
Used to update existing data.
 
🔧 Code:
```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_item": item}
```

🔗 URL:

PUT http://127.0.0.1:8000/items/2

📨 Sample Request Body:
```json
{
  "name": "Mouse",
  "price": 500
}
```

🔁 Sample Response:
```json
{
  "item_id": 2,
  "updated_item": {
    "name": "Mouse",
    "price": 500
  }
}
```
---

### 6. DELETE Endpoint
**✅ Description**:
Used to delete a resource.
 
🔧 Code:
```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted_item_id": item_id}
```

🔗 URL:
DELETE http://127.0.0.1:8000/items/10

🔁 Sample Response:
```json
{
  "deleted_item_id": 10
}
```

🧪 Testing with Postman
Open Postman
 
Choose HTTP method (GET, POST, etc.)
 
Enter the appropriate URL
 
For POST/PUT, go to Body → raw → JSON, and add the request body

---
## ✅ Summary Table
 
| Method | Endpoint              | Description         |
|--------|-----------------------|---------------------|
| GET    | `/`                   | Basic Hello World   |
| GET    | `/items/{item_id}`    | Get item by ID      |
| GET    | `/search/?q=value`    | Get using query     |
| POST   | `/items/`             | Create new item     |
| PUT    | `/items/{item_id}`    | Update an item      |
| DELETE | `/items/{item_id}`    | Delete an item      |
---