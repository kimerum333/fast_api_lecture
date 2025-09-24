from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth import oauth2
from src.db.database import get_db
from src.db.hash import Hash
from src.db.models import DbUser

router = APIRouter(
    tags=["authentication"],
)

router.post("/token")


def get_token(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="credit invalid",
        )
    if not Hash.verify(str(user.password), request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid password",
        )
    access_token = oauth2.create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "user_name": user.username,
    }
