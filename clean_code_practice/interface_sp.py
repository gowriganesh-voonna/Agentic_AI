# Interface segegration Principle
# The Interface Segregation Principle states that no client should be forced to depend on methods it does not use.
# This means that larger interfaces should be split into smaller, more specific ones so that clients only need to know about the methods that are of interest to them.


from abc import ABC, abstractmethod

# class Worker(ABC):
#     @abstractmethod
#     def work(self):
#         return "Working"
    
#     @abstractmethod
#     def eat(self):
#         return "Eating"
    
#     @abstractmethod
#     def code(self):
#         return "Coding"
    


# class HumanWorker(Worker):

#     def work(self):
#         return "Human Working"
    
#     def eat(self):
#         return "Human Eating"
    
#     def code(self):
#         return "Human Coding"

# class RobotWorker(Worker):
#     def work(self):
#         return "Robot Working"
    
#     def eat(self):
#         raise NotImplementedError("Robot does not eat")  # Robots do not eat
    
#     def code(self):
#         return "Robot Coding"
    
# def manage_worker(worker:Worker):
#     print(worker.work())
#     print(worker.eat())
#     print(worker.code())

# manage_worker(HumanWorker())
# manage_worker(RobotWorker())


# Solution: We can create separate interfaces for Workable and Eatable.

class Workable(ABC):
    @abstractmethod
    def work(self):
        pass
    
class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass
class Coding(ABC):
    @abstractmethod
    def code(self):
        pass
    
class HumanWorker(Workable,Eatable,Coding):
    def work(self):
        return "Human Working"
    
    def eat(self):
        return "Human Eating"
    
    def code(self):
        return "Human Coding"

class RobotWorker(Workable,Coding):   # Only implements Workable and Coding
    def work(self):
        return "Robot Working"
    
    def code(self):
        return "Robot Coding"
    

def manage_workable(worker:Workable):
    print(worker.work())

def manage_eatable(worker:Eatable):
    print(worker.eat())

def manage_coding(worker:Coding):
    print(worker.code())

manage_workable(HumanWorker())
manage_eatable(HumanWorker())
manage_coding(HumanWorker())

manage_workable(RobotWorker())
manage_coding(RobotWorker())