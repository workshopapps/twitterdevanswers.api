from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import MetaData
from app.database import Base, engine
from uuid import uuid4, UUID
import uuid as uuid_pkg
import sqlalchemy
import datetime
from sqlalchemy import types
from sqlalchemy_utils.types.choice import ChoiceType
metadata = MetaData()


class Transaction(Base):
    TYPES = [
        ('earned', 'Earned'),
        ('spent', 'Spent'),
    ]

    __tablename__ = 'transactions'
    __table_args__ = {'extend_existing': True}

    transaction_id = Column(String(50), primary_key=True, nullable=False)
    user_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=True)
    transacion_type = Column(ChoiceType(TYPES))
    amount = Column(Integer, default=0, nullable=False)
    description = Column(String(1024), nullable=True)
    transaction_date = Column(TIMESTAMP(timezone=True),
                              nullable=False, server_default=text('now()'))


class Wallet(Base):
    __tablename__ = 'walletaccount'
    __table_args__ = {'extend_existing': True}

    id = Column(String(50), primary_key=True)
    balance = Column(Integer, default=100, nullable=True)
    spendings = Column(Integer, default=0, nullable=False)
    earnings = Column(Integer, default=0, nullable=False)
    total_spent = Column(Integer, default=0, nullable=False)
    total_earned = Column(Integer, default=0, nullable=False)
    is_devask_wallet = Column(Boolean, default=False)
    user_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=True)
    created_at = Column(
        DateTime, default=datetime.datetime.utcnow, nullable=False)


class User(Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}
    user_id = Column(String(50), primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(30), nullable=True, default=" ")
    last_name = Column(String(30), nullable=True, default=" ")
    email = Column(String(100), nullable=False, unique=True)
    date_of_birth = Column(String(100), nullable=True, default=" ")
    gender = Column(String(7), nullable=False, default=" ")
    description = Column(String(400), nullable=True, default=" ")
    password = Column(String(200), nullable=False)
    phone_number = Column(String(30), nullable=True, default=" ")
    organization = Column(String(400), nullable=True, default=" ")
    work_experience = Column(String(400), nullable=True, default=" ")
    position = Column(String(400), nullable=True, default=" ")
    stack = Column(String(400), nullable=True, default=" ")
    links = Column(String(400), nullable=True, default=" ")
    role = Column(String(300), nullable=True)
    following = Column(Integer, nullable=True, default=0)
    followers = Column(Integer, nullable=True, default=0)
    image_url = Column(String(300), nullable=True, default=" ")
    location = Column(String(100), nullable=True, default=" ")
    is_admin = Column(Boolean, default=False)
    account_balance = Column(Integer, default=100)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    verification_code = Column(String(300), nullable=True, default=" ")
    is_verified = Column(Boolean, nullable=True, default=False)
    mfa_hash = Column(String(300))


class Following(Base):
    __tablename__ = "following"
    __table_args__ = {'extend_existing': True}
    user_from = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"
    ), nullable=True, primary_key=True)
    target_user = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"
    ), nullable=True, primary_key=True)


class Question(Base):
    __tablename__ = "question"
    __table_args__ = {'extend_existing': True}
    question_id = Column(String(50), primary_key=True, nullable=False)
    owner_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(400), nullable=False)
    content = Column(String(2000), nullable=False)

    expected_result = Column(String(2000), nullable=False)
    payment_amount = Column(Integer, nullable=False)

    answered = Column(Boolean, default=False, nullable=False)
    tag = Column(String(200), default=" ")
    total_like = Column(Integer, default=0)
    total_unlike = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    owner = relationship('model.User')
    tags = relationship(
        "model.Tag", secondary="question_tags", back_populates="questions")


class Answer(Base):
    __tablename__ = "answer"
    __table_args__ = {'extend_existing': True}
    answer_id = Column(String(50), primary_key=True, nullable=False)
    owner_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(String(50), ForeignKey(
        "question.question_id", ondelete="CASCADE"), nullable=False)
    content = Column(String(2000))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    is_answered = Column(Boolean, nullable=True)
    vote = Column(Integer, default=0)
    owner = relationship('model.User')
    question = relationship('model.Question')


class AnswerVote(Base):
    __tablename__ = "answer_vote"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    owner_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=True)
    answer_id = Column(String(50), ForeignKey(
        "answer.answer_id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(String(100), nullable=False)
    owner = relationship('model.User')
    answer = relationship('model.Answer')


class Like(Base):
    __tablename__ = 'likes'
    __table_args__ = {'extend_existing': True}

    like_id = Column(String(50), primary_key=True)
    item_type = Column(String(20), nullable=False , default = "None")
    item_id = Column(String(50), nullable=False)
    user_id = Column(String(50), ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)

    user = relationship('User') 


class Notification(Base):
    __tablename__ = "notification"
    __table_args__ = {'extend_existing': True}
    notification_id = Column(String(50), primary_key=True, nullable=False)
    owner_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content_id = Column(String(50), ForeignKey(
        "answer.answer_id", ondelete="CASCADE"), nullable=False)
    owner = relationship('model.User')
    # content = relationship('model.Answer')
    type = Column(String(200), nullable=False)
    unread = Column(Boolean, default=True)
    title = Column(String(200), nullable=False)


class NotificationTransaction(Base):
    __tablename__ = "transaction_notification"
    __table_args__ = {'extend_existing': True}
    notification_id = Column(String(50), primary_key=True, nullable=False)
    owner_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    content_id = Column(String(50), ForeignKey(
        "transactions.transaction_id", ondelete="CASCADE"), nullable=False)
    owner = relationship('model.User')
    content = relationship('model.Transaction')
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
    tag_id = Column(String(50), primary_key=True, nullable=False)
    tag_name = Column(String(40), nullable=False)
    questions = relationship("model.Question",
                             secondary="question_tags", back_populates="tags")


class Blog(Base):

    __tablename__ = 'blog'
    __table_args__ = {'extend_existing': True}
    blog_id = Column(String(50), primary_key=True, nullable=False)
    title = Column(String(300), nullable=False)
    body = Column(String(7000), nullable=False)
    author = Column(String(300), nullable=False)
    image_url = Column(String(300), default="default.jpg")
    post_category = Column(String(200), nullable=False)
    is_approved = Column(Boolean, default=False, nullable=False)
    user = relationship('model.User')
    date_posted = Column(TIMESTAMP(timezone=True),
                         nullable=False, server_default=text('now()'))
    blog_user_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)


class Community(Base):
    __tablename__ = 'community'
    __table_args__ = {'extend_existing': True}

    community_id = Column(String(50), primary_key=True, nullable=False)
    user_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(300), nullable=False,unique=True)
    description = Column(String(700), nullable=False)
    image_url = Column(String(300), default="default.jpg")
    total_members = Column(Integer, nullable=True, default=0)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    users = relationship(
        'model.User', secondary="community_members", backref="user")
    admins = relationship('model.User',secondary="community_admins",backref="user_admin")


community_members = Table('community_members', Base.metadata,
                          Column('community_id', ForeignKey(
                              'community.community_id'), primary_key=True),
                          Column('users', ForeignKey(
                              'user.user_id'), primary_key=True)
                          )

community_admins = Table('community_admins', Base.metadata,
                          Column('community_id', ForeignKey(
                              'community.community_id'), primary_key=True),
                          Column('admins', ForeignKey(
                              'user.user_id'), primary_key=True)
                          )


class Topic(Base):
    __tablename__ = 'topic'
    __table_args__ = {'extend_existing': True}

    community_id = Column(String(50), ForeignKey(
        "community.community_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    topic_id = Column(String(50), primary_key=True, nullable=False)
    title = Column(String(300), nullable=False)
    content = Column(String(10000), nullable=False)
    image_url = Column(String(300), default="default.jpg")
    is_approved = Column(Boolean, default=False, nullable=False)
    total_comments = Column(Integer, nullable=True , default=0)
    total_likes = Column(Integer, nullable=True , default=0)
    created_at = Column(TIMESTAMP(timezone=True),
                         nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('model.User')
    community = relationship('model.Community')


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {'extend_existing': True}

    topic_id = Column(String(50), ForeignKey(
        "topic.topic_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(50), ForeignKey(
        "user.user_id", ondelete="CASCADE"), nullable=False)
    comment_id = Column(String(50), primary_key=True, nullable=False)
    parent_comment_id = Column(String(50),nullable=False,default="None")
    total_reactions = Column(Integer, nullable=True , default=0)
    content = Column(String(700), nullable=False)
    image_url = Column(String(300), default="default.jpg")
    created_at = Column(TIMESTAMP(timezone=True),
                         nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('model.User')
    topic = relationship('model.Topic')





# create tables
Base.metadata.create_all(bind=engine)
