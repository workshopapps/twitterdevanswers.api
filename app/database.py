from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# devlopment
# SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:123456@localhost:5432/devask'

# production
#SQLALCHEMY_DATABASE_URI = "postgresql://rpiefrkjxxncgz:38a33ed0eb25a13b7f4f1d5bd02fee72bad4fc86cbd9d07df6d2bf1e35561890@ec2-44-199-143-43.compute-1.amazonaws.com:5432/d2kq6ba278qupb"
#SQLALCHEMY_DATABASE_URI = "mysql://devask:HNG#9devask@localhost/devask"
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:8566@localhost:5433/suppliers"
SQLALCHEMY_DATABASE_URI = "postgresql://qyevadrnislxhk:92e12d8bbe1a82d4c60f5b089bb1bd8fa2806880716828119220925f882446db@ec2-54-160-109-68.compute-1.amazonaws.com:5432/db61l29l5p66eb"
# SQLALCHEMY_DATABASE_URI = "mysql://devask:HNG#9devask@localhost/devask"

#engine = create_engine(SQLALCHEMY_DATABASE_URI)
engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='latin1', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
#Base.metadata.create_all(bind=engine)
        db.close()


# Base.metadata.create_all(bind=engine)
