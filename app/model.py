from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base, engine


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False)
    first_name = Column(String(30), nullable=False, default="firstname")
    last_name = Column(String(30), nullable=False, default="lastname")
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)
    #account_balance = Column(Integer)
    #role = Column(String(100))
    image_url = Column(String(300), default="default.jpg")


class Question(Base):
    __tablename__ = "question"
    __table_args__ = {'extend_existing': True}
    question_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content = Column(String(2000), nullable=False)
    answered = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner = relationship('app.model.User')


class Answer(Base):
    __tablename__ = "answer"
    __table_args__ = {'extend_existing': True}
    answer_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey(
        "question.question_id", ondelete="CASCADE"), nullable=False)
    content = Column(String(2000))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    is_answer = Column(Boolean, nullable=True)
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
    __table_args__ = {'extend_existing': True}
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey(
        'user.user_id', ondelete="CASCADE"), primary_key=True)
    question_id = Column(Integer, ForeignKey(
        'question.question_id', ondelete="CASCADE"), primary_key=True)


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = {'extend_existing': True}
    notification_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content_id = Column(Integer, ForeignKey(
        "answer.answer_id", ondelete="CASCADE"), nullable=False)
    owner = relationship('app.model.User')
    content = relationship('app.model.Answer')
    type = Column(String(200), nullable=False)
    unread = Column(Boolean, default=True)
    title = Column(String(200), nullable=False)


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = {'extend_existing': True}
    tag_id = Column(Integer, primary_key=True, nullable=False)
    tag_name = Column(String(40), nullable=False)


class contenTag(Base):

    __tablename__ = 'contenTag'
    __table_args__ = {'extend_existing': True}
    question_id = Column(Integer, ForeignKey(
        "question.question_id", ondelete="CASCADE"),  primary_key=True, nullable=False)
    tag_id = Column(Integer, ForeignKey(
        "tag.tag_id", ondelete="CASCADE"), nullable=False)
    question = relationship('app.model.Question')
    tag = relationship('app.model.Tag')


Base.metadata.create_all(bind=engine)
