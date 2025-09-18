from fastapi import FastAPI

from src.db import models
from src.db.database import engine
from src.routers import blog_get, blog_post, user

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)


@app.get("/")
def index():
    return "Hello World!"


models.Base.metadata.create_all(engine)
