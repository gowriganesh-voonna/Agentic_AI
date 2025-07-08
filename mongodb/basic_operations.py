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

#print(collection.find_one())  # no find or find_many will work

# inseting many dictionaries
# data = collection.insert_many( [
#     {"Name":"John", "age":25 , "Country":"USA","Salary":678900},
#     {"Name":"Abdhul kaju" , "age":56, "Country":"India","Disabilty":"Yes","Salary":34560},
#     {"Name":"Asha " , "age":45,"Salary":89000}

# ]
# )

# for d in collection.find():
#     print(d)

# filtered = collection.find({"Salary":
#                             {"$gt":50000}})

# print("Salary greater than >50000")
# for d in filtered:
#     print(d)


print("=================================================")

# nested_data = collection.insert_one(
#     {
#         "Name":"Pavan",
#         "Destignation":"CEO",
#         "Company" : "Human Empower",
#         "address" : {
#             "Door_No":"22-14/1-89/3",
#             "Area":"Madhapur",
#             "City":"Hyderabad"
#         }
#     }
# )

#print(collection.find_one({"Name":"Pavan"}))

# nested_data_many = collection.insert_many(
#     [
#     {
#         "Name":"Pavan",
#         "Destignation":"CEO",
#         "Company" : "Human Empower",
#         "address" : {
#             "Door_No":"22-14/1-89/3",
#             "Area":"Madhapur",
#             "City":"Hyderabad"
#         }
#     },
#     {
#         "Name":"Priyanka",
#         "Destignation":"MD",
#         "Company" : "Human Bank",
#         "address" : {
#             "Door_No":"22-1-3/A",
#             "Area":"Bhanu Nagar",
#             "City":"Vijayawada"
#         }

#     }

#     ]
# )


# it is not working
query0 = {"Name":{"$regx":r"^P","$options":"i"}}  # ^P means finding name with P stating letter and i is case sensitive

query = {
    "$expr":{
        "$eq":[
            {"$substr":["$Name",0,1]},
            "P"
        ]
    }
}
filtered=collection.find(query)

print("People Name whose started with P")

for d in filtered:
    print(d)

query = {
    "address.City":"Hyderabad"
}

results = collection.delete_one(query)

print("Deleted")

