from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# devlopment
# SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:123456@localhost:5432/devask'

# production
SQLALCHEMY_DATABASE_URI = "postgresql://qyevadrnislxhk:92e12d8bbe1a82d4c60f5b089bb1bd8fa2806880716828119220925f882446db@ec2-54-160-109-68.compute-1.amazonaws.com:5432/db61l29l5p66eb"
# SQLALCHEMY_DATABASE_URI = "mysql://devask:HNG#9devask@localhost/devask"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base.metadata.create_all(bind=engine)
