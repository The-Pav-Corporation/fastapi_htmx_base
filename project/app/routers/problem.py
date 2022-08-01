from ..dependencies import get_db
from ..util import crud
from ..schemas.problem import Problem
from ..solutions import solutions
from ..settings import templates

from fastapi import Depends, APIRouter, Form, Request, Response, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List, Union
import logging

_logger = logging.getLogger("uvicorn.error")

router = APIRouter(
    prefix="/problems",
    tags=["problems"]
)

@router.get("/", response_model=List[Problem])
def read_problems(request: Request, source: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    problems = crud.get_problems(db, skip, limit, source)
    return templates.TemplateResponse("problem/list.html", {"request": request, "problems": problems})

@router.get("/create")
def problem_create_page(request: Request):
    return templates.TemplateResponse("problem/create.html", {"request": request})

@router.post("/", response_model=List[Problem])
def create_problem(
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    source: str = Form(...),
    external_url: str = Form(""),
):
    if crud.get_problem_by_title(db=db, title=title):
        raise HTTPException(400, "Problem with this title already exists!")
    crud.create_problem(
        db=db,
        title=title,
        description=description,
        external_url=external_url,
        source=source
    )
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

@router.get("/{problem_id}")
def problem_detail(request: Request, problem_id: int, db: Session = Depends(get_db)):
    problem = crud.get_problem(db, problem_id)
    return templates.TemplateResponse("problem/detail.html", {"request": request, "problem": problem})

@router.get("/{problem_id}/edit")
def problem_edit(request: Request, problem_id: int, db: Session = Depends(get_db)):
    problem = crud.get_problem(db, problem_id)
    return templates.TemplateResponse("problem/edit.html", {"request": request, "problem": problem})

@router.post("/{problem_id}")
def problem_put(
    request: Request,
    problem_id: int,
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    external_url: str = Form(""),
    source: str = Form(...),
):
    problem = crud.edit_problem(db, problem_id, title, description, external_url, source)
    return templates.TemplateResponse("problem/detail.html", {"request": request, "problem": problem})


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
    return HTMLResponse(content=output.replace("\n", "<br/>"))
    
@router.get("/{problem_id}/mark_solved")
def problem_mark_solved(problem_id: int, db: Session = Depends(get_db)):
    db_problem = crud.get_problem(db, problem_id)
    if db_problem.is_solved:
        db_problem.is_solved = False
        solved = "Not solved"
    else:
        db_problem.is_solved = True
        solved= "Solved"
    db.commit()
    return HTMLResponse(content=solved)