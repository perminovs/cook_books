import sqlalchemy as sa
from pydantic import BaseSettings

from cool_books.db import Session


class CORSSettings(BaseSettings):
    enabled: bool = True
    origins: list[str] = ['http://localhost', 'http://localhost:8000']

    class Config:
        env_prefix = 'CORS_'


class DBSettings(BaseSettings):
    url: str = 'postgresql://postgres@localhost:5432/postgres'

    class Config:
        env_prefix = 'DB_'

    def setup(self, echo: bool = False) -> None:
        engine = sa.create_engine(url=self.url, echo=echo)
        Session.configure(bind=engine)
