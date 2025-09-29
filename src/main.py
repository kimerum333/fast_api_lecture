from fastapi import FastAPI, HTTPException, Request, status, Response
from fastapi.responses import JSONResponse, PlainTextResponse, HTMLResponse
from fastapi.websockets import WebSocket
from fastapi.staticfiles import StaticFiles

from src.auth import authentication
from src.db import models
from src.db.database import engine
from src.exceptions import StoryException
from src.routers import article, blog_get, blog_post, file, product, user
from src.client import html
import time
from typing import List

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
async def get_slash():
    return HTMLResponse(html)

clients:List[WebSocket] = []
@app.websocket("/chat")
async def websocket_endpoint(websocket:WebSocket):
    await websocket.accept()
    clients.append(websocket)
    while True:
        data = await websocket.receive_text()
        for client in clients:
            await client.send_text(data)


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
