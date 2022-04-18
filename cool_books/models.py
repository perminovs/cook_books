from typing import List, Optional

from pydantic import BaseModel, Field


class BookModel(BaseModel):
    id: int
    author: str
    title: str
    tag: str
    owner: str


class BookResponse(BaseModel):
    payload: List[BookModel]
    next_offset: Optional[str] = Field(None, alias='next')
