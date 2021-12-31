from typing import Optional
from fastapi import FastAPI
from sqlalchemy.orm import session
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:35000",
]

from model import db_session
import query
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return {"Hello": "World"}

@app.get("/user")
def get_users():
    session = db_session.session_factory()
    users = query.get_users(session=session)
    return users

@app.post("/user")
def create_user(name: str):
    session = db_session.session_factory()
    query.create_user(session, name)
    return

class MessageModel(BaseModel):
    message: str

@app.post("/message")
def create_message(data: MessageModel):
    session = db_session.session_factory()
    msg = query.create_message(session=session, message=data.message)
    return msg

@app.get("/message")
def get_message(q: Optional[str] = None):
    session = db_session.session_factory()
    return query.get_messages(session=session, query=q)