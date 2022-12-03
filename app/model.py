from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base, engine
from uuid import UUID
from sqlalchemy.dialects.mysql import UUID
import uuid as uuid_pkg
import sqlalchemy
import datetime


class Wallet(Base):
    __tablename__ = 'walletaccount'
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                server_default=sqlalchemy.text("gen_random_uuid()"),)
    balance = Column(Integer, default=1000, nullable=False)
    deposits_made = Column(Integer, default=0, nullable=False)
    spendings = Column(Integer, default=0, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False, default=" ")
    last_name = Column(String(30), nullable=False, default=" ")
    email = Column(String(100), nullable=False, unique=True)
    description = Column(String(400), nullable=True, default=" ")
    password = Column(String(200), nullable=False)
    phone_number = Column(String(30), nullable=True, default=" ")
    work_experience = Column(String(400), nullable=True, default=" ")
    position = Column(String(400), nullable=True, default=" ")
    stack = Column(String(400), nullable=True, default=" ")
    links = Column(String(400), nullable=True, default=" ")
    role = Column(String(300), nullable=True)
    following = Column(Integer, nullable=False, default=0)
    followers = Column(Integer, nullable=False, default=0)
    image_url = Column(String(300), default=" ")
    location = Column(String(100), nullable=True, default=" ")
    is_admin = Column(Boolean, default=False)
    account_balance = Column(Integer, default=1000)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Following(Base):
    __tablename__ = "following"
    __table_args__ = {'extend_existing': True}
    user_from = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"
    ), nullable=False, primary_key=True)
    target_user = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"
    ), nullable=False, primary_key=True)


class Question(Base):
    __tablename__ = "question"
    __table_args__ = {'extend_existing': True}
    question_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(400), nullable=False)
    content = Column(String(2000), nullable=False)

    expected_result = Column(String(2000), nullable=False)
    payment_amount = Column(Integer, nullable=False)

    answered = Column(Boolean, server_default='FALSE', nullable=False)
    tag = Column(String(200), default=" ")
    total_like = Column(Integer, default=0)
    total_unlike = Column(Integer, default=0)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner = relationship('app.model.User')
    # tags = relationship(
    #     "app.model.Tag", secondary="question_tags", backref="questions")

    tags = relationship(
        "app.model.Tag", secondary="question_tags", back_populates="questions")


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
    is_answered = Column(Boolean, nullable=True)
    vote = Column(Integer, default=0)
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
    __table_args__ = {'extend_existing': True}
    like_id = Column(Integer, primary_key=True)
    like_type = Column(String(100), nullable=False)
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


question_tags = Table(
    "question_tags",
    Base.metadata,
    Column("question_id", ForeignKey(
        "question.question_id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.tag_id"), primary_key=True),
    extend_existing=True
)


class Tag(Base):
    __tablename__ = 'tag'
    __table_args__ = {'extend_existing': True}
    tag_id = Column(Integer, primary_key=True, nullable=False)
    tag_name = Column(String(40), nullable=False)
    questions = relationship("app.model.Question",
                             secondary="question_tags", back_populates="tags")


@compiles(DropTable, "postgresql")
def _compile_drop_table(element, compiler, **kwargs):
    return compiler.visit_drop_table(element) + " CASCADE"


Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)
# Base.metadata.reflect()
# Base.metadata.clear()
# Base.metadata.remove(User.__table__)
