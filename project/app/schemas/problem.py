from pydantic import BaseModel
from typing import List, Optional


class ProblemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ProblemCreate(ProblemBase):
    pass


class Problem(ProblemBase):
    id: int
    input: str = None
    solution: str = None
    is_solved: bool = False

    class Config:
        orm_mode = True
