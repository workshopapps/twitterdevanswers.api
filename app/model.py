from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    account_balance = Column(Integer)
    role = Column(String(100))
    image_url = Column(String(300))


class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content = Column(String(2000), nullable=False)
    answered = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner = relationship('User')


class Answer(Base):
    __tablename__ = "answer"
    answer_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey(
        "question.question_id", ondelete="CASCADE"), nullable=False)
    owner = relationship('User')
    question = relationship('question')


class Notification(Base):
    __tablename__ = "notification"
    notification_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content_id = Column(Integer, ForeignKey(
        "answer.answer_id", ondelete="CASCADE"), nullable=False)
    owner = relationship('user')
    content = relationship('answer')
    type = Column(String(200), nullable=False)
    unread = Column(Boolean, default=True)
    title = Column(String(200), nullable=False)


class Tag(Base):
    __tablename__ = 'tag'
    tag_id = Column(Integer, primary_key=True, nullable=False)
    tag_name = Column(String(40), nullable=False)


class contenTag(Base):
    __tablename__ = 'contenTag'
    question_id = Column(Integer, ForeignKey(
        "question.question_id", ondelete="CASCADE"),  primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey(
        "tag.tag_id", ondelete="CASCADE"), nullable=False)
    question = relationship('question')
    tag = relationship('tag')
