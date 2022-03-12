from sqlalchemy.orm import Session
from .. import models
from .. schemas import item as item_schema, user as user_schema, problem as problem_schema

import logging

_logger = logging.getLogger("uvicorn.error")

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schema.UserCreate):
    fake_hashed_password = f'{user.password}notreallyhashed'
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: item_schema.ItemBase, user_id: int):
    db_item = models.Item(**item.dict(),owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Problems
def get_problems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Problem).offset(skip).limit(limit).all()

def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem).filter(models.Problem.id == problem_id).first()

def get_problem_by_title(db: Session, title: str):
    return db.query(models.Problem).filter(models.Problem.title == title).first()

def create_problem(db: Session, title, description):
    db_problem = models.Problem(title=title, description=description)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    _logger.debug(db_problem)
    return db_problem

def delete_problem(db: Session, problem_id: int):
    db.delete(get_problem(db=db, problem_id=problem_id))
    db.commit()