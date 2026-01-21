# lsp : liskov substitution principle
# A derived class should be substitutable for its base class without altering the correctness of the program.


# class Bird:
#     def fly(self):
#         return "Flying"
    

# class Sparrow(Bird):
#     def fly(self):
#         return "Sparrow flying"
    
# class Penguin(Bird):
#     def fly(self):
#         raise Exception("Penguins can't fly") 
    
# def make_bird_fly(bird:Bird):
#     return bird.fly()

# print(make_bird_fly(Sparrow()))
# print(make_bird_fly(Penguin())) # This will raise an exception, violating LSP.

# Solution: We can create a separate base class for flying birds and non-flying birds to adhere to LSP.

# from abc import ABC, abstractmethod

# class FlyingBird(ABC):
#     @abstractmethod
#     def fly(self):
#         pass

# class swimmingBird(ABC):
#     @abstractmethod
#     def swim(self):
#         pass

# class NonFlyingBird(ABC):
#     @abstractmethod
#     def walk(self):
#         pass


# class Sparrow(FlyingBird):
#     def fly(self):
#         return super().fly()
    
# class Penguin(swimmingBird,NonFlyingBird):
#     def swim(self):
#         return super().swim()
    
#     def walk(self):
#         return super().walk()
    
# class Eagle(FlyingBird):
#     def fly(self):
#         return super().fly()
    

# def make_bird_fly(bird:FlyingBird):
#     return bird.fly()

# def make_bird_swim(bird:swimmingBird):
#     return bird.swim()

# def make_bird_walk(bird:NonFlyingBird):
#     return bird.walk()

# print(make_bird_fly(Sparrow()))
# print(make_bird_swim(Penguin()))
# print(make_bird_walk(Eagle())) # This will raise an exception, violating LSP.


class Bird:
    def move(self):
        return "Moving"
    
class FlyingBirdBird(Bird):
    def move(self):
        return "FLying"
    

class SwimmingBird(Bird):
    def move(self):
        return "swimming"
    
class Sparrow(FlyingBirdBird):
    pass

class Penguin(SwimmingBird):
    pass

class Eagle(FlyingBirdBird):
    pass

def make_bird_move(bird:Bird):
    print(bird.move()) # works for any bird subclass without issues

make_bird_move(Sparrow())
make_bird_move(Penguin())
make_bird_move(Eagle())
# opened closed principle

