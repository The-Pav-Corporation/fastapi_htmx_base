from ..dependencies import get_db
from ..util import crud
from ..schemas.problem import Problem, ProblemCreate

from fastapi import Depends, APIRouter, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/problems",
    tags=["problems"]
)

@router.get("/", response_model=List[Problem])
def read_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_problems(db, skip=skip, limit=limit)

@router.post("/", response_model=Problem)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    if crud.get_problem_by_title(db=db, title=problem.title):
        raise HTTPException(400, "Problem with this title already exists!")
    return crud.create_problem(db=db, problem=problem)

@router.delete("/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    crud.delete_problem(db=db, problem_id=problem_id)
    return Response(content="Deleted problem", status_code=status.HTTP_204_NO_CONTENT)
