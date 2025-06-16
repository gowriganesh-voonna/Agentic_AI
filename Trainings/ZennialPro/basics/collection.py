# List operations
fruits = ['apple', 'banana', 'orange','graps']
fruits.append('grape')     # Add item
fruits.insert(0, 'kiwi')  # Insert at position
print("fruits")
print(f"After sortation {fruits.sort()}")


# Tuples
point =(1,4)
x,y = point # Tuple Unpacking
print(f"X{x} , y:{y}")   # printing tuple
coordinates =(*point,y)
print(f"Coordinates of X(Addreess) and y {coordinates}")

# Dictionary 
user_data ={
    "name":"Voonna",
    "Roll_number" : 123 ,
  " is_activate" : True
}

# dictionary acceess

print(f"Dictionary print method :{user_data}")


# DIctionary comarison

squres =[ lambda x:x**2 for x in range(4)]

print(squres)

squares2 = squres ={ lambda x:x**2 for x in range(4)}

print(squares2)


# Working with binary data
bytes_data = bytes([65, 66, 67])  # Creates b'ABC'
bytearray_data = bytearray(bytes_data)  # Mutable bytes

print(f"Bytes_data in ABC {bytes_data}")
print(f"bytearray_data : {bytearray_data}")