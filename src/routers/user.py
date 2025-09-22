from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import db_user
from src.db.database import get_db
from src.schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


# create user
@router.post("/", response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# update user
@router.put("/{id}")
def update_user(id: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)


# read all user
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# read one user
@router.get("/{id}", response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_user(db, id)


# delete user
@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)
