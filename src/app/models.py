from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

from .db import ENGINE, BaseModel


class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    messages = relationship(
        "Message",
        cascade="save-update, merge, delete, delete-orphan",
        backref=backref("message"),
    )


class Message(BaseModel):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow().replace(microsecond=0))
    scheduled = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    kind = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", backref=backref("user"))


BaseModel.metadata.create_all(bind=ENGINE)
