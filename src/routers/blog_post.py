from typing import List, Optional

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

router = APIRouter(prefix="/blog", tags=["blog"])


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
    comments_number: int


@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "data": blog,
        "id": id,
        "version": version,
    }


@router.post("/new/{id}/comment/{comment_id}")
def create_comment(
    blog: BlogModel,
    id: int,
    comment_title: str = Query(
        None,
        title="Id of the comment",
        description="some description for comment_title",
        alias="commentId",
        deprecated=True,
        regex=r"^[a-z\s]*$",  # 정규표현식으로도 검증 가능
    ),
    v: Optional[List[str]] = Query(["1.1", "1.3"]),
    comment_id: int = Path(
        gt=5,
        le=10,
    ),
    content: str = Body("hi, how are you"),
):
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "v": v,
        "comment_id": comment_id,
    }
