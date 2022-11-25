from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# devlopment
#SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:123456@localhost:5432/devask'

# production
SQLALCHEMY_DATABASE_URI = "postgresql://rpiefrkjxxncgz:38a33ed0eb25a13b7f4f1d5bd02fee72bad4fc86cbd9d07df6d2bf1e35561890@ec2-44-199-143-43.compute-1.amazonaws.com:5432/d2kq6ba278qupb"

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
