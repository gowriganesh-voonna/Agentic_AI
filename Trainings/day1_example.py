def analyze_grade():

   try:
     #get scores from the user
     maths_score = float(input("Please Enter the maths Sxore :"))
     science_score = float(input("\n Please Enter the science score :"))
     if maths_score < 0 or science_score< 0:
        raise ValueError("Scores cannot be negative")
   except ValueError as e:
        print(f"\nInvalid data type {e}")
    #Calculating the average
   average = (maths_score + science_score)/2

   if average>80:
        performance = "Outstanding"
   elif average > 60:
        performance="Good"
   else :
        performance="Bad"

    #Display the average and performance grade
   print(f"The average of the student is {average} and performance is {performance}")

analyze_grade()

