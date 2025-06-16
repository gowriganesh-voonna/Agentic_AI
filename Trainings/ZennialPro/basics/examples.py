def student_profile():
    """creating an function with student profile"""
    student_name = "Voonna Gowri Ganesh"
    college_name = "SRK Institute of Technology"
    final_grade = 70.5
    is_passed = True

    
    # Print Profile with Proper formatting.
    print(f"Student Profile")
    print(f"Name : { student_name}(Type :{type(student_name)})")
    print(f"college name : {college_name} (Type: {type(college_name)})")
    print(f"Final Grade : {final_grade}(Type : {type(final_grade)})")
    print(f"IS Passed {is_passed} (Type : {type(is_passed)})")


def calculator():
    """this function will return all arithemetic operations"""

    # get user input
    num1=float(input("Please Enter the number :"))
    num2 = float(input("Please enter the 2nd number :"))
    #dictionary
    operations ={
        "Addition" : num1+num2,
        "Subraction": num1-num2,
        "Muiltipication ": num1*num2,
        "Division" : num1/num2 if num2 !=0 else "Error : Zero Divison Error",
        "Modulo "   : num1%num2 if num2!=0 else "Error : Zero Divison Error",
        "Floor "    : num1//num2 if num2!=0 else "Error : Zero Divison Error",
        "Exponent"  : num1 ** num2 
    }
     # displaying operations by using for loop
    for  operation, result in operations.items():
        print(f"{operation}  : {result}")



def student_grade_analyer():
    """this function takes input from the user and displays his grade and subject scores."""
    math_score = float(input("Enter the math score :"))
    science_score = float(input("Enter the science score :"))

    average_score =(math_score+science_score)/2

    if average_score>=80:
        grade="Out_Standing"
    elif average_score>=70:
        grade="Good"
    elif average_score>=50:
        grade="Average"
    elif average_score>=35:
        grade="Poor"
    else:
        grade="Need to Improve Performance"

    print(f"Grade of the Student is {grade}")
    print(f"Total_score : {math_score+science_score}")
    print(f"Average Score : {average_score}")
    print(f"Math_Score : {math_score}")
    print(f"science_score : {science_score}")


def process_cart():
    products = {
        "Laptop": 99909,
        "Mobile": 50000,
        "Tablets": 30000
    }

    # empty cart for storing user products
    cart = []
    print("------Available Products--------------")
    while True:
        for product, price in products.items():
            print(f"Product: {product}, Price: {price}")

        user_input = input("Please enter the product name or enter ('done') if you completed: ").strip().lower()

        if user_input == "done":
            break
        elif user_input.capitalize() in products:
            quantity = int(input("Enter the quantity: "))
            cart.append({
                "Product_Name": user_input.capitalize(),
                "price": products[user_input.capitalize()],
                "Quantity": quantity
            })
        else:
            print("Product Not Found")

    print("------------Total Bill ---------")
    total_price = 0
    for item in cart:
        item_total = item["price"] * item["Quantity"]
        print(f"{item['Product_Name']} x{item['Quantity']}: ₹{item_total:.2f}")
        total_price += item_total

    print(f"Total Amount Payable: ₹{total_price:.2f}")
process_cart()
        
