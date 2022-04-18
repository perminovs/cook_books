import sqlalchemy as sa
import sqlalchemy.orm as so

from cool_books import db
from cool_books.settings import DBSettings


def main() -> None:
    settings = DBSettings()
    settings.setup()
    db.Base.metadata.bind = sa.create_engine(url=settings.url)
    db.Base.metadata.drop_all()
    db.Base.metadata.create_all()

    with db.create_session() as session:
        _create_unit(session, 'history', 'Roland', 'Lord of the Rings I')
        _create_unit(session, 'history', 'Grigor', 'Lord of the Rings II')


def _create_unit(session: so.Session, tag_name: str, user_name: str, book_title: str) -> None:
    tag = session.query(db.Tag).filter(db.Tag.name == tag_name).one_or_none() or db.Tag(name=tag_name)
    user = db.User(nickname=user_name)
    book = db.Book(author='Tolkien', title=book_title, owner=user, tag=tag)
    session.add_all((tag, book, user))
    session.flush()
    exchange = db.Exchange(book_id=book.id, tag_id=tag.id)
    session.add(exchange)


if __name__ == '__main__':
    main()
