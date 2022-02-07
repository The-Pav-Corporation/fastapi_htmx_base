from .settings import templates

from fastapi import Depends, FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from .routers.token import router as token_router
from .routers.user import router as user_router
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(token_router)
app.include_router(user_router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("shared/_layout.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_root(request: Request, token: str = Depends(oauth2_scheme)):
    return templates.TemplateResponse("admin/index.html", {"request": request, "token": token})

@app.get("/clicked")
async def clicked():
    content=str(4+7)
    return HTMLResponse(content=content)
