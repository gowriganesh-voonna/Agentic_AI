
class Car:
    wheels=4

    def __init__(self,make:str,model:str,year:int):
        self.make=make
        self.model=model
        self.year=year

BMW=Car("BMW","Petrol",2025)
print(BMW.wheels)
print(BMW.make)