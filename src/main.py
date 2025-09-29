from fastapi import FastAPI, HTTPException, Request, status, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from src.auth import authentication
from src.db import models
from src.db.database import engine
from src.exceptions import StoryException
from src.routers import article, blog_get, blog_post, file, product, user
import time

app = FastAPI()
app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)

@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response:Response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response

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


app.mount(
    "/files",  # endpoint
    StaticFiles(directory="files"),  # mountpoint
    name="files",
)

models.Base.metadata.create_all(engine)
