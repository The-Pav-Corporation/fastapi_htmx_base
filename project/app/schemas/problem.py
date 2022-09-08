from pydantic import BaseModel, validator
from typing import List, Optional


class ProblemBase(BaseModel):
    title: str
    description: Optional[str] = None

    @validator('*')
    def field_has_printable_chars(self, value):
        if "\x00" in value:
            raise ValueError("Field value has unprintable characters.")

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
