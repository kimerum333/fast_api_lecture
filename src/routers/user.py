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
# read user
# delete user
