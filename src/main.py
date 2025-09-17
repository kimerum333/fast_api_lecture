from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

@app.get('/')
def index():
    return "Hello World!"

@app.get('/blog/all')
def get_all_blogs(page: int = 1 , page_size: Optional[int] = None):
    return {"message" : f"All {page_size} blogs on {page}"}

@app.get('/blog/{id}') # 패스에 {}로 id 를 잡아와 캡처
def get_blog_by_id(id: int):         # 인자로 id 를 주고,
    return {"message" : f"Blog with id {id}"} #함수 내부 사용

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'

@app.get('/blog/type/{type}')
def get_blog_type(type: BlogType):
    return {"message" : f"Blog type: {type}"}