# #list
# student_lists=["Voonna","Gowri","Ganesh"]

# #dict  key-> value pairs
# student_marks={"Voonna":67,
#                "Gowri": 70,
#                "Ganesh": 45}

# print(student_lists)
# print(student_marks)


#key : value -> Int, string, dict, list

# employee_details = {
#     "Voonna" : {"Employee_Id":1, "Department":"IT_Developer"},
#     "Surendhra" : { "Employee Id":2, "Department":"IT_Developer"},
#     "Gannu": {"Employee Id":3, "Department":"Tester"},
#     "Pavani":{"Employee Id":4, "Department":"HR"},
#     "Gannu1" : {"Employee Id":3, "Department":"Firewall"}
# }

# print(employee_details["Gannu1"])
# print(employee_details["Voonna"]["Employee_Id"])
# print(employee_details["Gannu"]["Department"])


# dictionary method using for loop.

student_details = {
    "Id1":"Voonna Gowri Ganesh",
    "Id2" : " G surendhra reddy",
    "Id3" : " M Venkata Prem Shankar",
    "Id4" : "Nunna Vijay Sai"
}

for key, value in student_details.items():
    print(key,"->",value)

# now adding one value to the dict
student_details["Id5"]="Voonna Naga Pranathi"

#now updating the value of the key of the dictionary
student_details["Id5"]="Voonna Gannu"

print(student_details)

# by using get method 
print(student_details.get("Id2"))
print(student_details.get("Voonna"))   # It will print None instead of rasing error.

# by using items
d = {'Name': 'Ram', 'Age': '19', 'Country': 'India'}
print(list(d.items())[0][1])
print(list(d.items())[1][1])

print(d.items())

print(d.values())  # printing only values 

# now using pop method 
print(d.pop("Age"))

# pop item is used toremove last key value pair.
print(d.popitem())


# by using fromkeys

x=("Key1","key2","key3")
y=3

thisdict=dict.fromkeys(x,y)
print(thisdict)