
from fastapi import APIRouter,HTTPException, Query
from typing import List,Optional
from datetime import datetime

from app.models.task import TaskBase,TaskCreate,TaskUpdate,Task,DeleteTask 
from app.data.file_data import load_json,save_json
from app.utiles.decoratores import handle_exceptions
from app.utiles.loggers import get_logger

router = APIRouter()
logger = get_logger(__name__)

FILE_PATH = "app/data/task.json"

def generate_new_id(tasks:List[dict]) ->int:
    if not tasks:
        return 1
    return max( task["id"] for task in tasks)+1

@handle_exceptions
@router.post("/create_task",response_model=Task)
async def create_task(task:TaskCreate):
    """Create_task will create new record in .json file and return
    to the user."""
    tasks = await load_json(FILE_PATH)

    new_task = {
        "id":generate_new_id(tasks), # Generate unique ID
        "title":task.title,
        "description":task.description,
        "status":task.status,
        "priority":task.priority,
        "deadline":task.deadline.isoformat(), # Serialize datetime
        "assigned_to":task.assigned_to,
        "created_at":datetime.now().isoformat() # Add timestamp
    }

    tasks.append(new_task)
    save_json(FILE_PATH,tasks)

    logger.info(f"Task created : {new_task["id"]}")

    return new_task

# Get all tasks with optional filters
@handle_exceptions
@router.get("/all_tasks",response_model=List[Task])
async def get_tasks(
    status : Optional[str] = Query(None,description="Filter by status"),
    priority : Optional[str] = Query(None,description="Filter by priority"),
    assigned_to : Optional[str] = Query(None,description="Filter by assigned_to")

):
    tasks = await load_json(FILE_PATH)
    now = datetime.now()

    # Log warning for overdue tasks
    
    for task in tasks:
        deadline_dt = datetime.fromisoformat(task["deadline"])

        if deadline_dt < now and task["status"] != "Completed":
            logger.warning(f"Task {task['id']} is overdue !")

    if status:
        tasks = [t for t in tasks if t["status"]==status]

    if priority:
        tasks = [t for t in tasks if t["priority"] == priority]
    if assigned_to:
        tasks= [t for t in tasks if t["assigned_to"]==assigned_to]
    
    return tasks

# Get a single task by ID
@handle_exceptions
@router.get("/get_by_task_id/{task_id}",response_model=Task)
async def get_task(task_id:int):
    tasks = await load_json(FILE_PATH)

    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404,detail=f"Task {task_id} not found")

# Update a task by ID
@handle_exceptions
@router.put("/tasks/{task_id}")
async def update_task(task_id:int,update_task : TaskUpdate):
    tasks = await load_json(FILE_PATH)
    found = False

    for task in tasks:
        print("----------")
        print(task)
        if task["id"] == task_id:
            found = True
            task["title"] = update_task.title or task["title"]
            task["description"] = update_task.description or task["description"]
            task["status"] = update_task.status or task["status"]
            task["priority"] = update_task.priority or task["priority"]
            # task["deadline"] = update_task.deadline.isoformat() or task["deadline"]
            if update_task.deadline is not None:
                task["deadline"] = update_task.deadline.isoformat()
            task["assigned_to"] = update_task.assigned_to or task["assigned_to"]
            break
    if not found:
        raise HTTPException(status_code=404,
                            detail=f"Task {task_id} not found")
    save_json(FILE_PATH,tasks)
    logger.info(f"Task Updated : {task_id}")
    return {"Message":f"Task_id {task_id} has been updated successfully"}

# Delete a task by ID and title
@handle_exceptions
@router.delete("/delete_task/{task_id}")
@handle_exceptions
async def delete_task(task_id : int,remove_task:DeleteTask):
    tasks = await load_json(FILE_PATH)  # need to write await  keyword if not coroutine error will occurs

    # Remove task that matches both ID and title
    new_tasks = [task for task in tasks if not(task["id"]== task_id and task["title"] == remove_task.title)]

    if len(tasks) == len(new_tasks):
        raise HTTPException(status_code=404,
                            detail=f"Task_id {task_id} not found")
    
    save_json(FILE_PATH,new_tasks)
    logger.info(f"Task_id Deleted : {task_id} ")
    return {"Message":f"Task_id {task_id} deleted successfully"}

