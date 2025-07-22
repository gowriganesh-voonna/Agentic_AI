import dspy

class IsEligible(dspy.Predict):
    def __init__(self):
        super().__init__(signature="name , age -> message")

    def forward(self,name:str,age:int) ->str:
        if age>=18:
            return f"{name} is eligible for vote."
        elif age>=0 and age<18:
            return f"{name} you are not eligible for vote."
        else:
            return "Something wrong"
        

iseligible= IsEligible()
print(iseligible(name="Voonna",age=23))