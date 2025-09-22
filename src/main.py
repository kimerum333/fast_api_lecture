from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse

from src.db import models
from src.db.database import engine
from src.exceptions import StoryException
from src.routers import article, blog_get, blog_post, user

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)


@app.get("/")
def index():
    return "Hello World!"


@app.exception_handler(StoryException)
def story_exception_handler(request: Request, exc: StoryException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"detail": exc.name},
    )


@app.exception_handler(HTTPException)
def custom_exception_handler(request: Request, exc: HTTPException):
    return PlainTextResponse(str(exc), status_code=400)


models.Base.metadata.create_all(engine)
