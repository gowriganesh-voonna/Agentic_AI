from pymongo import MongoClient

Mongo_Url = "mongodb+srv://gowriganeshvoonna:3EhpwdUK0FnSh3YP@resume-data.wz0y1el.mongodb.net/"
DB_NAME = "Resume_db"
sample_data = "sample_data"

client = MongoClient(Mongo_Url)
database = client[DB_NAME]
collection = database[sample_data]

# data = collection.insert_one({
#     "Name":"Ganesh",
#     "Age":22,
#     "City":"Vijayawada",
#     "Salary":40000,
#     "Company":"Zennial Pro"
# })

print(collection.find_one())  # no find or find_many will work

# inseting many dictionaries
# data = collection.insert_many( [
#     {"Name":"John", "age":25 , "Country":"USA","Salary":678900},
#     {"Name":"Abdhul kaju" , "age":56, "Country":"India","Disabilty":"Yes","Salary":34560},
#     {"Name":"Asha " , "age":45,"Salary":89000}

# ]
# )

for d in collection.find():
    print(d)