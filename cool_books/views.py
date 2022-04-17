from typing import List, Optional, Type

import sqlalchemy.orm as so
from fastapi import Depends, HTTPException

from cool_books import db
from cool_books.models import BookModel, BookResponse, SessionData, cookie

BOOK_PAGE_SIZE = 20


def create_exchange(book_id: int, tag_id: int, session_data: SessionData = Depends(cookie)) -> None:
    with db.create_session() as session:
        book = (
            session.query(db.Book)
            .filter(db.Book.id == book_id, db.Book.owner_id == session_data.user_id)
            .one_or_none()
        )
        if not book:
            raise HTTPException(status_code=404, detail='Book not found')

        exchange = db.Exchange(receiver_id=session_data.user_id, book_id=book_id, tag_id=tag_id)
        session.add(exchange)


def get_exchanges(offset: Optional[int] = None, session_data: SessionData = Depends(cookie)) -> BookResponse:
    with db.create_session() as session:
        my_book: Type[db.Book] = so.aliased(db.Book)
        target_book: Type[db.Book] = so.aliased(db.Book)
        my_exchange: Type[db.Exchange] = so.aliased(db.Exchange)
        target_exchange: Type[db.Exchange] = so.aliased(db.Exchange)

        books_query = (
            session.query(target_book)
            .join(target_exchange, target_book.id == target_exchange.book_id)
            .join(my_book, my_book.tag_id == target_exchange.tag_id)
            .join(my_exchange, my_exchange.book_id == my_book.id)
            .filter(
                target_exchange.receiver_id.is_(None),
                my_exchange.receiver_id.is_(None),
                target_book.owner_id != session_data.user_id,
                my_book.owner_id == session_data.user_id,
            )
        )
        if offset:
            books_query = books_query.filter(db.Book.id < offset)
        books_query = books_query.order_by(db.Book.id.desc()).limit(BOOK_PAGE_SIZE)
        books: List[db.Book] = books_query.all()

        payload = [
            BookModel(id=b.id, author=b.author, title=b.title, tag=b.tag.name, owner=b.owner.nickname) for b in books
        ]

    next_offset = f'/exchange?offset={payload[-1].id}' if payload else None
    return BookResponse(payload=payload, next_offset=next_offset)
