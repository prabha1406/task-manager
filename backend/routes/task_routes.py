from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import User
from backend.models import Task
from backend.schemas import TaskCreate
from backend.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(title=task.title)
    db.add(new_task)
    db.commit()
    return new_task

@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.put("/tasks/{id}")
def update_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    task.completed = True
    db.commit()
    return {"message": "Updated"}

@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return {"message": "Deleted"}
@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_user = db.query(User).filter(User.username == user).first()

    new_task = Task(title=task.title, owner_id=db_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
@router.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    completed: bool | None = None
):
    db_user = db.query(User).filter(User.username == user).first()

    query = db.query(Task).filter(Task.owner_id == db_user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    return query.offset(skip).limit(limit).all()
@router.put("/tasks/{id}")
def update_task(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_user = db.query(User).filter(User.username == user).first()

    task = db.query(Task).filter(Task.id == id, Task.owner_id == db_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()

    return {"message": "Task completed"}
@router.delete("/tasks/{id}")
def delete_task(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_user = db.query(User).filter(User.username == user).first()

    task = db.query(Task).filter(Task.id == id, Task.owner_id == db_user.id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Deleted"}