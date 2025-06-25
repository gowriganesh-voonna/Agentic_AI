from app.data.file_data import load_json,save_json
from app.models.students import Student
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger


logger = get_logger(__name__)
DATA_PATH = "app/data/students.json"

students = load_json(DATA_PATH)

@handle_exceptions
def add_student():

    student= Student(
        student_id= input("Enter Student_id :").strip(),
        name = input("Enter name :").strip(),
        branch = input("Enter Branch Name :").strip(),
        year = int(input("Enter the year :"))

    )

    students.append(student.dict())
    save_json(DATA_PATH,students)
    logger.info(f"Student_id : {student.student_id} Added Successfully")
    print(f"Student_id : {student.student_id} Added Successfully")



@handle_exceptions
def view_all_students():
    logger.info(f"View all Students Method is called")
    print(students)


@handle_exceptions
def update_student():
    student_id = input("Enter student_id for update :").strip()
    exists = any(s["student_id"] == student_id for s in students )
    if not exists:
        logger.info(f"Student_id : {student_id} Not Found")
        raise ValueError(f"Student_ID : {student_id} not found")
    
    for s in students:

        if s["student_id"] == student_id:
            s["name"] = input("Enter New Name :").strip() or s["name"]
            s["branch"] = input("Enter the branch or leave blank :").strip() or s["branch"]

            while True:
                year= int(input("Enter the year b/w 1 to 4 :"))

                if not year:
                    break
                if 1 <= year <= 4:
                    s["year"] = year
                    break
                else:
                    print("Year should be in b/w 1 to 4")
    save_json(DATA_PATH,students)
    logger.info(f"Student_id : {student_id} Updated Succeessfully")
    print(f"Student_id : {student_id} Updated Succeessfully")



@handle_exceptions
def search_student():
    text = input("Enter student_id or name :").strip()
    result = list(filter(lambda s:text in s["student_id"] or text in s["name"],students))

    if not result:
        logger.info(f" Student Not found : {text}")
        print("Details Not Found")
    else :
        logger.info(f" Displaying Search Result" )
        print(f"{result} added successfully")
        

@handle_exceptions
def remove_student():
     student_id = input("Enter the Student_id").strip()
     exists = any(s["student_id"] == student_id for s in students )

     if not exists:
        logger.info(f"Student_id : {student_id} Not Found")
        raise ValueError(f"Student_ID : {student_id} not found")
     name = input("Enter the name :").strip()

     filtered = [s for s in students if s["student_id"]!= student_id and s["name"]!= name]

     save_json(DATA_PATH,filtered)
     logger.info(f"Student : {student_id} Deleted succeesfully")
     print(f"Student : {student_id} Deleted succeesfully")


    # "student_id": "S001",
    # "name": "Alice",
    # "branch": "CS",
    # "year": 2