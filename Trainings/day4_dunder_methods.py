# dunder methods : also unknown as magic method or special methods that allow you to define the behaviour of your custom objects.
# with respect to built in operations like printing,arithematic operations,comprison,iterations and more.

class Person:
    def __init__(self,name):
        self.name=name  #Instance varible
        self.data = {}  #Instance specific dictionary or set
        print(self.name)

    def __str__(self):            # Informal string 
        return f"This is my  {self.name} name"    #Returns human redable string representations

    def __repr__(self):
        return f"Person(name='{self.name}')"    # formal Representation  - return unambiguous string representation .
    def __len__(self):
        return len(self.data)

    def __getitems__(self,key):
        return self.data.get(key,None)

    def __setitem__(self,key,value):
        self.data[key]=value 

    def __call__(self):
        return f"{self.name} this was called like an function"

    def __enter__(self):
        return f"This enter magic method is executed"   
    def do_something(self):
        return f"I will do cleaning now"

    def __exit__(self,exc_type,exc_val,exc_tab):
        print(f"Exit method is going to executed.")

    def __eq__(self,other):
        return isinstance(other,Person) and self.name == other.name
    def __del__(self):
        return f"This methd   {self.name}is going to execute or destroyed"

# person1=Person("Voonna")   # object

# print(str(person1))
# print(str(Person(name="Gowri")))

# print(repr(person1))
# print(len(person1))

obj=Person(name="Voonna")
obj["Voonna"]="GOwri"

print(len(obj))

with obj:
    print(obj.do_something)
    print("With block executed")

print(obj== Person("Voonna"))

del obj