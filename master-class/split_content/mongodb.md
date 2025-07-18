- Visit [https://cloud.mongodb.com](https://cloud.mongodb.com)
- Create a free cluster, database `bookstore`, collection `books`
- Whitelist your IP and get connection URI
- Store the connection string securely in `.env` file
 
```dotenv
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/bookstore?retryWrites=true&w=majority
```

----

## Section 8.11:📌 MongoDB Operations using `pymongo.MongoClient`
 
### 🔧 Setup MongoClient
 
```python
from pymongo import MongoClient
 
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]
```
### Section 8.12:✅ Insert a Single Document
```python
def insert_single_document():
    document = {"name": "Alice", "age": 25, "city": "New York"}
    result = collection.insert_one(document)
    print("Inserted ID:", result.inserted_id)
```

### Section 8.13:✅ Insert Multiple Documents
```python
def insert_multiple_documents():
    documents = [
        {"name": "Bob", "age": 30, "city": "Chicago"},
        {"name": "Charlie", "age": 28, "city": "San Francisco"},
    ]
    result = collection.insert_many(documents)
    print("Inserted IDs:", result.inserted_ids)
```

### Section 8.14:🔍 Search Documents
```python
def find_all_documents():
    docs = collection.find()
    for doc in docs:
        print(doc)
 
def find_by_filter():
    query = {"city": "New York"}
    docs = collection.find(query)
    for doc in docs:
        print(doc)
```
