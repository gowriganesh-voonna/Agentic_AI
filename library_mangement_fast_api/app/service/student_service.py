from app.data.file_data import load_json,save_json
from app.models.students import Student,UpdateStudent,SearchStudent,RemoveStudent
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger
from fastapi import APIRouter,HTTPException
from typing import List

DATA_PATH = "app/data/students.json"

logger = get_logger(__name__)
router = APIRouter()


students = load_json(DATA_PATH)

@handle_exceptions
@router.post("/add_student")
async def add_student(student: Student):

    students.append(student.dict())
    save_json(DATA_PATH,students)
    refresh_students()
    logger.info(f"Student_id : {student.student_id} Added Successfully")
    return {"Message":f"Student_id : {student.student_id} Added Successfully"}



@handle_exceptions
@router.get("/view_all_students",response_model=List[Student])
async def view_all_students():
    logger.info(f"View all Students Method is called")
    return students


@handle_exceptions
@router.put("/update_student")
async def update_student(student: UpdateStudent):
    student_id = student.student_id.strip()
    exists = any(s["student_id"] == student_id for s in students )
    if not exists:
        logger.info(f"Student_id : {student_id} Not Found")
        raise HTTPException(status_code= 404,
                             detail=f" {student_id}Details Not Found")
    
    for s in students:

        if s["student_id"] == student_id:
            s["name"] = student.name or s["name"]
            s["branch"] = student.branch or s["branch"]

            while True:
                year= student.year

                if not year:
                    break
                if 1 <= year <= 4:
                    s["year"] = year
                    break
                else:
                    raise HTTPException(status_code=400, detail="Year should be between 1 and 4")
    save_json(DATA_PATH,students)
    refresh_students()
    logger.info(f"Student_id : {student_id} Updated Succeessfully")
    return {"Message":f"Student_id : {student_id} Updated Succeessfully"}



@handle_exceptions
@router.post("/search_student",response_model=List[Student])
async def search_student(student : SearchStudent):
    text = student.query.strip()
    result = list(filter(lambda s:text in s["student_id"] or text in s["name"],students))

    if not result:
        logger.info(f" Student Not found : {text}")
        raise HTTPException(status_code= 404,
                             detail="Details Not Found")
    logger.info(f" Displaying Search Result" )
    return result
        

@handle_exceptions
@router.delete("/remove_student")
async def remove_student(student : RemoveStudent):
     before = len(students)
     student_id = student.student_id.strip()
     exists = any(s["student_id"] == student_id for s in students )

     if not exists:
        logger.info(f"Student_id : {student_id} Not Found")
        raise HTTPException(status_code=404, detail=f"Student_ID : {student_id} not found")
       
     name = student.name.strip()

     filtered = [s for s in students if not (s["student_id"]== student_id and s["name"]== name)]

     after = len(filtered)

     if before == after:
        raise HTTPException(status_code=404, detail="Student not found or name mismatch")

     save_json(DATA_PATH,filtered)
     refresh_students()
     logger.info(f"Student : {student_id} Deleted succeesfully")
     return {"Message":f"Student : {student_id} Deleted succeesfully"}


    # "student_id": "S001",
    # "name": "Alice",
    # "branch": "CS",
    # "year": 2


def refresh_students():
    global students
    students = load_json(DATA_PATH)