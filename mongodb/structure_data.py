from pymongo import MongoClient

Mongo_Url = "mongodb+srv://gowriganeshvoonna:3EhpwdUK0FnSh3YP@resume-data.wz0y1el.mongodb.net/"
DB_NAME = "Resume_db"
sample_data = "sample_data"

client = MongoClient(Mongo_Url)
database = client[DB_NAME]
collection = database[sample_data]

# data = collection.insert_many(
#     [
#         {
#         "Customer ID":"CUST002",
#         "Name":"Pavan Kumar",
#         "Email":"krkpavan@gmail.com",
#         "Details":{
#             "Address":{
#                 "Door_No":"22-1-3/A",
#                 "Area":"Maruthi Nagar",
#                 "City":"Vijayawada",
#                 "Pincode":"520012"
#             },
#             "CustomerCare":{
#                 "ExecutiveName":"Priya Sharma",
#                 "Contact":["+918798056798","+9188853541"],
#                 "Email":"support@flipkart.com"
#             },
#             "Payments":{
#                 "PaymentMethod":["Credit Card","Debit Card"],
#                 "Card":345,
#                 "UPI_ID" : "PhoneUPI@upi",
#                 "SubscriptionType":"Standard"
#             },
#             "Orders":[
#                 {
#                     "OrderID":"ORD00A1",
#                     "OrderType":"Standard",
#                     "Items":[
#                         {
#                             "ProductID":"PH001",
#                             "ProductName":"Samsung J13",
#                             "Status":"Delivered"
#                         },
#                         {
#                            "ProductID":"PH0023",
#                             "ProductName":"Ear Phones",
#                             "Status":"Shipped"  
#                         }
#                     ]
#                 }
#             ]
#         }
#     },


#     {
#         "Customer ID":"CUST003",
#         "Name":"Vijay Reddy Nunna",
#         "Email":"nunnavijaysai@gmail.com",
#         "Details":{
#             "Address":{
#                 "Door_No":"23-12-45/A",
#                 "Area":"Vijayawada Central Jail",
#                 "City":"Vijayawada",
#                 "Pincode":"520045"
#             },
#             "CustomerCare":{
#                 "ExecutiveName":"Priya Sharma",
#                 "Contact":["+918798056798","+9188853541"],
#                 "Email":"support@flipkart.com"
#             },
#             "Payments":{
#                 "PaymentMethod":["Credit Card","Debit Card","Cash-on-Delivery"],
            
#                 "SubscriptionType":"Standard",
                
#             },
#             "Orders":[
#                 {
#                     "OrderID":"ORD120",
#                     "OrderType":"Standard",
#                     "Items":[
#                         {
#                             "ProductID":"D001",
#                             "ProductName":"Inner Wears",
#                             "Status":"Delivered"
#                         },
#                         {
#                            "ProductID":"P003",
#                             "ProductName":"shampoo",
#                             "Status":"Shipped"  
#                         }
#                     ]
#                 }
#             ]
#         }
#     }
#     ]
# )

print("==============================Insertion Success============================")
print("---------------------------Filtering Data---------------------------------")

query = {"Details.Payments.SubscriptionType":"Standard"}

filtered = collection.find(query)

for d in filtered:
    print(d)

print("-------------------------------------------------")
print("------------------------Filtered ends name with ra")


#================== see structure_data.txt file for explanation
query1 = {
    "$expr":{
        "$eq":[
            {
                "$substrCP" : [
                    "$Name",
                    { "$subtract":[{"$strLenCP":"$Name"},2]},
                    2
                ]
            },
            "ar"
        ]
    }
}
filtered1 = collection.find(query1)


for d in filtered1:
    print(d)