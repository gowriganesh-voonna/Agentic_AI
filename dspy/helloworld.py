import dspy


class Helloworld(dspy.Predict):
    def __init__(self):
        super().__init__(signature="username->message")

    def forward(self,name:str)->str:
        return f"Hello {name} welcome to Dspy"
    

predictor = Helloworld()

print(predictor(name="Voonna"))