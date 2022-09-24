from sqlalchemy import Boolean, Column, Integer, String, VARCHAR

from .database import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    source = Column(String, index=True)
    description = Column(String, index=True)
    input = Column(String, index=True, default=None)
    solution = Column(String, index=True, default=None)
    is_solved = Column(Boolean, default=False)
    external_url = Column(VARCHAR(100), default=None)
