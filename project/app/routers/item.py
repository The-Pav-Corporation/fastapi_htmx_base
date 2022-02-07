from ..dependencies import get_db
from ..util import crud
from ..schemas.item import Item, ItemCreate

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip=skip, limit=limit)
