import logging
from urllib import parse

from starlette.config import Config
from starlette.datastructures import Secret

log = logging.getLogger(__name__)

config = Config(".env")

# database
DB_DRIVER = config("DB_DRIVER")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME", default="fastapi")

DB_CREDENTIALS = config("DB_CREDENTIALS", cast=Secret)
_DB_CREDENTIAL_USER, _DB_CREDENTIAL_PASSWORD = str(DB_CREDENTIALS).split(":")
_QUOTED_DB_PASSWORD = parse.quote(str(_DB_CREDENTIAL_PASSWORD))

DB_ENGINE_POOL_SIZE = config("DB_ENGINE_POOL_SIZE", cast=int, default=20)
DB_ENGINE_MAX_OVERFLOW = config("DB_ENGINE_MAX_OVERFLOW", cast=int, default=0)
DB_ENGINE_POOL_PING = config("DATABASE_ENGINE_POOL_PING", default=False)

SQLALCHEMY_DATABASE_URI = f"{DB_DRIVER}://{_DB_CREDENTIAL_USER}:{_QUOTED_DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"