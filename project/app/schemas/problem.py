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
    source: str = None
    solution: str = None
    is_solved: bool = False
    external_url: str = None

    class Config:
        orm_mode = True
