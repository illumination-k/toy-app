from typing import List, Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import desc

from model import User, Message

import logging

logger = logging.getLogger(__name__)

def create_user(session: Session, name: str) -> Optional[User]:
    user = session.add(User(name=name))
    session.commit()
    return user

def get_users(session: Session) -> Optional[List[User]]:
    users = session.query(User).all()
    return users


def get_messages(*, session: Session, query: Optional[str] = None, limit: int = 10) -> Optional[List[Message]]:
    q = session.query(Message)
    if query is not None:
        q = q.filter(Message.message.like(f"%{query}%"))
    messages = q.order_by(desc(Message.created_at)).limit(limit).all()
    return messages


def create_message(*, session: Session, message: str) -> Optional[Message]:
    message = session.add(Message(message=message))
    session.commit()
    return message
