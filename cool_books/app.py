from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from cool_books.settings import CORSSettings
from cool_books.views import create_exchange, get_exchanges


def get_app() -> FastAPI:
    app = FastAPI()

    cors_settings = CORSSettings()
    if cors_settings.enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_settings.origins,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )

    app.get('/exchange')(get_exchanges)
    app.put('/exchange/{book_id}', status_code=201)(create_exchange)

    return app
