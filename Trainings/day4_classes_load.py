
class User:
    def __init__(self,name,age):
        self.name=name
        self.age=age

    #Displaying user information
    def __str__(self):
        return f"User name : {self.name} and his age is {self.age}"

    @classmethod
    def show_user(cls,data):
        name,age= data.split("-")
        return cls(name.strip(),int(age))

    @staticmethod
    def is_valid_age(age:int):
        return age>18

user=User("Voonna",22)
print(str(user))
print(user.show_user("      Voonna - 23"))


# class Instance creation = using class method
data_string="Gowri Ganesh - 22"
user1=User.show_user(data_string)
user_age = User.is_valid_age(23)
print(user_age)