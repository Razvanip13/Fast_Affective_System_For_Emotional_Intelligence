import domain.models
from sqlalchemy import create_engine
from sqlmodel import Session

DATABASE_URL = 'postgresql://postgres:l3tm3kn0w@localhost:5432/ThesisDB'
engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
