from cool_books.app import get_app
from cool_books.settings import DBSettings

DBSettings().setup()
app = get_app()
