from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from app.models import *
from app.schemas import CreateTask, UpdateTask
from app.backend.db_depends import get_db
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    ts = db.scalars(select(Task)).all()
    return ts

@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task1 = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Task was not found'
        )

    return task1

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user1 = db.scalars(select(User).where(User.id == user_id)).first()
    if user1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'User was not found'
        )

    db.execute(insert(Task).values(title = create_task.title,
                                    content = create_task.content,
                                    priority = create_task.priority,
                                    user_id = user1.id,
                                    slug = slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.post('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id:int, update_task: UpdateTask):
    task1 = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Task was not found'
        )

    db.execute(update(Task).where(Task.id == task_id).values(
                                    content = update_task.content,
                                    priority = update_task.priority))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.post('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id:int):
    task1 = db.scalars(select(Task).where(Task.id == task_id)).first()
    if task1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'Task was not found'
        )

    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task deleted successfully!'}

