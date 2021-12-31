import os
import sqlalchemy

from sqlalchemy import Column
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import ARRAY, DateTime, Float, Integer, String, TEXT

def get_postgres_url():
    url = os.environ.get("DATABASE_URI")
    if url is not None:
        return url

    if os.path.exists("/.dockerenv"):
        return "postgresql://postgres:postgres@postgres:5432/main"

    return "postgresql://postgres:postgres@localhost:5433/main"


def create_engine() -> Engine:
    if os.environ.get("DEBUG") is not None:
        echo = True
    else:
        echo = False
    return sqlalchemy.create_engine(get_postgres_url(), encoding="utf-8", echo=echo)


Engine = create_engine()

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=Engine)
)

Base = declarative_base()

# declare for query
Base.query = db_session.query_property()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(TEXT, nullable=False)
    created_at = Column(DateTime, server_default=func.now())