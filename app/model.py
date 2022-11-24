from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base, engine


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False)
    first_name = Column(String(30), nullable=False, default = "firstname")
    last_name = Column(String(30), nullable=False, default = "lastname")
    email = Column(String(100), nullable=False, unique=True)
    description = Column(String(400),nullable=True)
    password = Column(String, nullable=False)
    image_url = Column(String(300),default="default.jpg")
    location = Column(String(100),nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    account_balance = Column(Integer, default = 1000)


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
    content = Column(String(2000))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    is_answered = Column(Boolean,nullable=True)
    vote = Column(Integer)
    owner = relationship('app.model.User')
    question = relationship('app.model.Question')


class AnswerVote(Base):
    __tablename__ = "answer_vote"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=True)
    answer_id = Column(Integer, ForeignKey(
        "answer.answer_id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(String(100), nullable=False)
    owner = relationship('app.model.User')
    answer = relationship('app.model.Answer')


class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey(
        'user.user_id', ondelete="CASCADE"), primary_key=True)
    question_id = Column(Integer, ForeignKey(
        'question.question_id', ondelete="CASCADE"), primary_key=True)


class Notification(Base):
    __tablename__ = "notification"
    notification_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content_id = Column(Integer, ForeignKey(
        "answer.answer_id", ondelete="CASCADE"), nullable=False)
    owner = relationship('User')
    content = relationship('Answer')
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
    question = relationship('Question')
    tag = relationship('Tag')


Base.metadata.create_all(bind=engine)
