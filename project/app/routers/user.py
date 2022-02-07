from ..dependencies import get_db
from ..util.auth import get_current_active_user
from ..util import crud
from ..schemas.user import User, UserCreate
from ..schemas.item import Item, ItemCreate

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db=db, email=user.email):
        raise HTTPException(400, "Email already registered!")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@router.get("/{id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(404, "User not found!")
    return db_user

@router.post("/{id}/items", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return crud.create_user_item(db, item, user_id)
