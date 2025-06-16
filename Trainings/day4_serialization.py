#Problem statement
# User class will take two parameters which is name, age
# load the user class from JSON
# Serialization -> Process of converting an object into JSON or XML or CSV or custom(Text)
# Deserilaization -> Process of converting file (Json or xml or csv or custom(text)) into an objct

import json 

class User:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def to_dic(self):
        return {"Name:" : self.name, "age:" : self.age}
        
    def save_to_file(self,filename):
        with open(filename,"w") as f:
            json.dump(self.to_dic(),f)

    @classmethod
    def load_file(cls,filename):
        with open(filename,"r") as f:
            data=json.load(f)
        return cls(data['Name:'],data['age:'])


user=User("Voonna",22)   # Object stores in memory(Binary)
# user.save_to_file("voonna.json")  # Object stores in text format 
# print("File saved now executing load_file function")
# print(user.load_file("voonna.json"))

    
print(f"Load user : {user.name} and his age is {user.age}")
