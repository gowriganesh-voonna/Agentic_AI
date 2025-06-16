
details = { "name" : "Voonna",
           "age" : 22}

def greet(name,age):
    print(f"Hello Mrs.{name} your age : {age}")

#greet(details["name "],details["age "])

greet(**details) # Will uppack -> **kwargs -> **person = "name=Ameyaan", "age=50"