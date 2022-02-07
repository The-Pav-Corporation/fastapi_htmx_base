from datetime import timedelta
from ..fake_db.db import fake_users_db
from ..schemas.token import Token
from ..settings import ACCESS_TOKEN_EXPIRE_MINUTES
from ..util.auth import authenticate_user,create_access_token

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from logging import Logger

_logger = Logger(__name__)

router = APIRouter(
    prefix="/token",
    tags=["token"]
)

@router.post("/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}