from sqlalchemy.orm.session import Session

from src.db.hash import Hash
from src.db.models import DbUser
from src.schemas import UserBase


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()  # 자동 생성 ID 가 이 시점에 DB에서 생겨난다.
    db.refresh(new_user)  # 자동생성된 ID를 받아오기 위한 리프래시
    return new_user
