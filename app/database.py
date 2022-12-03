from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# devlopment
# SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
# SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:123456@localhost:5432/devask'

# production
# SQLALCHEMY_DATABASE_URI = "mysql://devask:HNG#9devask@localhost/devask"
SQLALCHEMY_DATABASE_URI = "postgresql://://hswuttzzoonnuj:84da1bb239e309794b0e3d88aebbc5d8069e908be6667a86e990d31759cf3d22@ec2-54-160-109-68.compute-1.amazonaws.com:5432/dcv4jf04kkfo1d"
# SQLALCHEMY_DATABASE_URI = "mysql://devask:HNG#9devask@localhost/devask"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# engine = create_engine(SQLALCHEMY_DATABASE_URI, encoding='latin1', echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# Base.metadata.create_all(bind=engine)
        # db.close()


# Base.metadata.create_all(bind=engine)
