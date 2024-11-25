from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from app.models import *
from app.schemas import CreateUser, UpdateUser
from app.backend.db_depends import get_db
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    us = db.scalars(select(User)).all()
    return us

@router.get('/{user_id}')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: str):
    user1 = db.scalars(select(User).where(User.id == user_id))
    return user1

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username = create_user.username,
                                    firstname = create_user.firstname,
                                    lastname = create_user.lastname,
                                    age = create_user.age,
                                    slug = slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.post('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], user_id:int, update_user: UpdateUser):
    user1 = db.scalars(select(User).where(User.id == user_id))
    if user1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'User was not found'
        )

    db.execute(update(User).where(User.id == user_id).values(
                                    username = update_user.username,
                                    firstname = update_user.firstname,
                                    lastname = update_user.lastname,
                                    age = update_user.age,
                                    slug = slugify(update_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.post('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id:int):
    user1 = db.scalars(select(User).where(User.id == user_id))
    if user1 is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'User was not found'
        )

    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}