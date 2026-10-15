from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from resources.db_creds import MoviesDbCreds

USER = MoviesDbCreds.USER
PASSWORD = MoviesDbCreds.PASSWORD
HOST = MoviesDbCreds.HOST
PORT = MoviesDbCreds.PORT
NAME = MoviesDbCreds.NAME

engine = create_engine(
    f"postgresql+psycopg://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}",
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()