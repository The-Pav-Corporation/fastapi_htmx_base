from .settings import templates

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from .routers.problem import router as problem_router
from . import models
from .database import engine

import logging

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(problem_router)

_logger = logging.getLogger("uvicorn.error")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("shared/index.html", {"request": request})
