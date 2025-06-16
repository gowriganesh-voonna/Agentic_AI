# lambda function : A lambda function in Python is a small, anonymous function defined using the lambda keyword. 
#It can take any number of arguments but can only have one expression. Lambda functions are often used for short, simple 
#operations where a full function definition is unnecessary. They are particularly useful in higher-order functions like map, 
#filter, and sorted. 

from functools import reduce
#reduce : it reduces the iterable list into an single value

numbers=[1,2,3,4,5]
square_numbers=list(map(lambda x:x**2,numbers))
print(square_numbers)   # printing square numbers

# filtering only even numbers into the list.
even_numbers=list(filter(lambda x:x%2 ==0,numbers))
print(even_numbers)

#reduce  
# [ 1+ 2 =3,
#   3+3=6,
#   6+4=10,
# 10+5=]

reduced_list= reduce(lambda x,y: x+y, numbers)
print(reduced_list)