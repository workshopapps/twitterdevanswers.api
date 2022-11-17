from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base


    
class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(15), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    account_balance = Column(Integer)
    role= Column(String(100))
    image_url = Column(String(300))

class Question(Base):
    __tablename__ = "question"
    question_id = Column(Integer, primary_key=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(String(2000))

    owner = relationship('User')

    
class Answer(Base):
    pass

class Notification(Base):
    pass

class Tage(Base):
    pass 






