# writing an code for printing weekday in an optimizied way

def get_day(day:str)->str:
    return {
        "Monday" : "WorkDay",
        "Tuesday":"WorkDay",
        "Wednesday":"Please Planning for Weekend",
        "Thursday":"Apply for an 2 days leave",
        "Friday":"Enjoy your leaves",
        "Saturday":"Enjoy your saturday",
        "Sunday":"Enjoy half day and prepare back to work from tomorrow."
    }.get(day,"Enter the correct day")


day=input("Enter the Day ".strip())

print(get_day(day))