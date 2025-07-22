import dspy

class ProductDetails(dspy.Predict):
    def __init__(self):
        super().__init__(signature = "product_name,value -> message")

    def forward(self,product_name:str,value:int) -> str:
        if product_name and value:
            return f"Product_name : {product_name} $ {value} Added Successfully"
        else:
            return f"Run again"
        
product_details = ProductDetails()
print(product_details(product_name = "Milk",value =43))