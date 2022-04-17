from contextlib import contextmanager
from typing import TYPE_CHECKING, Iterator

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import sessionmaker

if TYPE_CHECKING:
    from typing_extensions import TypeAlias

PK_TYPE = sa.BigInteger


class _Base:
    id = sa.Column(PK_TYPE, primary_key=True)


Base: 'TypeAlias' = so.as_declarative()(_Base)  # type: ignore


class User(Base):
    __tablename__ = 'user'

    nickname = sa.Column(sa.Text, nullable=False, unique=True)


class Tag(Base):
    __tablename__ = 'tag'

    name = sa.Column(sa.Text, nullable=False, unique=True)


class Book(Base):
    __tablename__ = 'book'

    author = sa.Column(sa.Text, nullable=False)
    title = sa.Column(sa.Text, nullable=False)
    owner_id = sa.Column(sa.ForeignKey(User.id), nullable=False, index=True)
    tag_id = sa.Column(sa.ForeignKey(Tag.id), nullable=False, index=True)

    owner: User = so.relationship(User, uselist=False, lazy='joined')
    tag: Tag = so.relationship(Tag, uselist=False, lazy='joined')


class Exchange(Base):
    __tablename__ = 'exchange'

    receiver_id = sa.Column(sa.ForeignKey(User.id), nullable=True)
    book_id = sa.Column(sa.ForeignKey(Book.id), nullable=False, index=True)
    tag_id = sa.Column(sa.ForeignKey(Tag.id), nullable=False)


Session = sessionmaker()


@contextmanager
def create_session() -> Iterator[so.Session]:
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
