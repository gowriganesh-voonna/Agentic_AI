
from fastapi import APIRouter,HTTPException, Query
from typing import List,Optional
from datetime import datetime

from app.models.task import TaskBase,TaskCreate,TaskUpdate,Task 
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
    tasks = load_json(FILE_PATH)

    new_task = {
        "id":generate_new_id(tasks),
        "title":task.title,
        "description":task.description,
        "status":task.status,
        "priority":task.priority,
        "deadline":task.deadline.isoformat(),
        "assigned_to":task.assigned_to,
        "created_at":datetime.now().isoformat()
    }

    tasks.append(new_task)
    save_json(FILE_PATH,tasks)

    logger.info(f"Task created : {new_task["id"]}")

    return new_task


@handle_exceptions
@router.get("/all_tasks",response_model=List[Task])
async def get_tasks(
    status : Optional[str] = Query(None,description="Filter by status"),
    priority : Optional[str] = Query(None,description="Filter by priority"),
    assigned_to : Optional[str] = Query(None,description="Filter by assigned_to")

):
    tasks = load_json(FILE_PATH)
    now = datetime.now()

    # log overdue tasks
    get_task =[]
    for task in tasks:
        deadline_dt = datetime.fromisoformat(task["deadline"])

        if deadline_dt < now and task["status"] != "Completed":
            logger.warning(f"Task {task['id']} is overdue !")

    if status:
        get_task = [t for t in tasks if t["status"]==status]

    if priority:
        get_task = [t for t in tasks if t["priority"] == priority]
    if assigned_to:
        get_task = [t for t in tasks if t["assigned_to"]==assigned_to]
    
    return get_task

@handle_exceptions
@router.get("/get_by_task_id/{task_id}",response_model=Task)
async def get_task(task_id:int):
    tasks = load_json(FILE_PATH)

    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404,detail=f"Task {task_id} not found")