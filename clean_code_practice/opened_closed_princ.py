# class Rectangle:
#     def __init__(self,height,width):
#         self.height=height
#         self.width=width

# class Circle:
#     def __init__(self,radius):
#         self.radius=radius



# class AreaCalculator0:
#     def calculate(self,shape):
#         if isinstance(shape, Rectangle):
#             return shape.height * shape.width
#         elif isinstance(shape, Circle):
#             return 3.14*shape.radius**2
#         else:
#             raise TypeError("Unsupported shape type")
        

# # Example usage:
# rectangle = Rectangle(5,10)
# circle = Circle(7)


# # drawback of this approach is that every time we add a new shape, we need to modify the AreaCalculator class.


# print("Area of Rectangle:",AreaCalculator().calculate(rectangle))
# print("Area of Circle:",AreaCalculator().calculate(circle))




# Solution : We can add a method to each shape class to calculate its area, adhering to the Open/Closed Principle.

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Rectangle(Shape):
    def __init__(self,height,width):
        self.height=height
        self.width=width

    def area(self):
        return self.height * self.width


class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius

    def area(self):
        return 3.14*self.radius**2
    

class Triangle(Shape):
    def __init__(self,base,height):
        self.base=base
        self.height=height

    def area(self):
        return 0.5*self.base*self.height
    
class AreaCalculator:

    def calculate(self,shape:Shape):
        return shape.area()
    

#Example usage:

rectangle = Rectangle(5,20)
circle= Circle(7)
triangle=Triangle(4,10)


print(f"Area of Rectangle: {AreaCalculator().calculate(rectangle)}")
print(f"Area of Circle: {AreaCalculator().calculate(circle)}")
print(f"Area of Triangle: {AreaCalculator().calculate(triangle)}")
