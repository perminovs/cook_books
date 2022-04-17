from typing import List, Optional

from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from pydantic import BaseModel, Field

cookie_params = CookieParameters()
cookie = SessionCookie(
    cookie_name='cookie',
    identifier='user_id',
    auto_error=True,
    secret_key='SECRET_KEY',
    cookie_params=cookie_params,
)


class SessionData(BaseModel):
    user_id: int


class BookModel(BaseModel):
    id: int
    author: str
    title: str
    tag: str
    owner: str


class BookResponse(BaseModel):
    payload: List[BookModel]
    next_offset: Optional[str] = Field(None, alias='next')
