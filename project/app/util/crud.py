from sqlalchemy.orm import Session
from .decorators.cleaners import ensure_printable
from .. import models

import logging

_logger = logging.getLogger("uvicorn.error")

# Problems
def get_problems(db: Session, skip: int = 0, limit: int = 100, source: str = None):
    if source:
        return db.query(models.Problem).filter(models.Problem.source == source).offset(skip).limit(limit)
    return db.query(models.Problem).offset(skip).limit(limit).all()

def get_problem(db: Session, problem_id: int):
    return db.query(models.Problem).filter(models.Problem.id == problem_id).first()

def get_problem_by_title(db: Session, title: str):
    return db.query(models.Problem).filter(models.Problem.title == title).first()

@ensure_printable
def create_problem(db: Session, title, description, external_url, source):
    db_problem = models.Problem(
        title=title,
        description=description,
        external_url=external_url,
        source=source,
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    _logger.debug(f"created: {db_problem}")
    return db_problem

def delete_problem(db: Session, problem_id: int):
    db.delete(get_problem(db=db, problem_id=problem_id))
    db.commit()

@ensure_printable
def edit_problem(db: Session, problem_id: int, title, description, external_url, source):
    db_problem = get_problem(db, problem_id)
    db_problem.title = title
    db_problem.description = description
    db_problem.external_url = external_url
    db_problem.source = source
    _logger.debug(f"edited: {db_problem.title}")
    db.commit()
    db.refresh(db_problem)
    return db_problem

