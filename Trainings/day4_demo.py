
class Demo:
    class_var=[]

    def __init__(self,name):
        self.name=name
        self.instance_var=[]


user1=Demo("Gowri")
user1.class_var.append("Added user1 obj to the class_var")
user1.instance_var.append("Added user1 obj to the instance_var")

print(user1.class_var)
print(user1.instance_var)