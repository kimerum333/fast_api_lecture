from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.db import db_article
from src.db.database import get_db
from src.schemas import ArticleBase, ArticleDisplay

router = APIRouter(
    prefix="/article",
    tags=["article"],
)


# Create
@router.post("/", response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.create_article(db, request)


# Get One
@router.get("/{id}", response_model=ArticleDisplay)
def get_article(id: int, db: Session = Depends(get_db)):
    return db_article.get_article(db, id)
