from ..dependencies import get_db
from ..util import crud
from ..schemas.problem import Problem
from ..components.problems import problem_create_view, problem_list_view, problem_detail_view
from ..solutions import solutions

from fastapi import Depends, APIRouter, Form, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import logging

_logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/problems",
    tags=["problems"]
)

@router.get("/", response_model=List[Problem])
def read_problems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # sourcery skip: move-assign-in-block, use-join
    content = ""
    for problem in crud.get_problems(db, skip=skip, limit=limit):
        content += problem_list_view(problem.title, problem.description, problem.id)
    return HTMLResponse(content=content)

@router.get("/create")
def problem_create_page():
    return HTMLResponse(content=problem_create_view())

@router.post("/", response_model=List[Problem])
def create_problem(
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
):
    if crud.get_problem_by_title(db=db, title=title):
        raise HTTPException(400, "Problem with this title already exists!")
    crud.create_problem(db=db, title=title, description=description)
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/{problem_id}")
def problem_detail(problem_id: int, db: Session = Depends(get_db)):
    db_problem = crud.get_problem(db, problem_id)
    return HTMLResponse(content=problem_detail_view(db_problem))

@router.get("/{problem_id}/delete")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    crud.delete_problem(db=db, problem_id=problem_id)
    url = router.url_path_for("read_problems")
    return RedirectResponse(url=url)

@router.post("/{problem_id}/solve")
def problem_solve(
    problem_id: int,
    db: Session = Depends(get_db),
    problem_input: str = Form(...),
):
    db_problem = crud.get_problem(db, problem_id)
    solution = solutions.get(db_problem.title.lower())
    output = solution(problem_input) if solution else "No solution found!"
    return HTMLResponse(content=output)
    
@router.get("/{problem_id}/mark_solved")
def problem_mark_solved(problem_id: int, db: Session = Depends(get_db)):
    db_problem = crud.get_problem(db, problem_id)
    content = ""
    if db_problem.is_solved:
        db_problem.is_solved = False
        content = "Unverified"
    else:
        db_problem.is_solved = True
        content = "Verified"
    db.commit()
    return HTMLResponse(content=content)