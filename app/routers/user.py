import sys
sys.path.append('..')
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from typing import List
from app.model import *
from app.database import get_db
from app import crud
from app import schema , oauth


router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# response model not working (response_model=schema.User)
@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   
    """ Get all users  """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get('/{username}',response_model=schema.User,response_model_exclude_unset=True)
def fetch_user(username:str, db: Session = Depends(get_db)):
    
    """ Fetch a user by it's user_id  """
    user = crud.get_user(db, username=username)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f" user  {username} not found")
    return user

# update returning null
@router.patch('/edit/{username}', response_model=schema.UserUpdate)
def update_user(user: schema.UserUpdate, username: str, db: Session = Depends(get_db)):
    
    """ Update a User profile by user_id  """
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user=user, username=username)


@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    """ Delete a user by it's user_id  """
  
    delete_user = crud.delete_user(db, user_id=user_id)
    if  delete_user is None:
        raise HTTPException(
            status_code=404, detail=f"user with id {user_id} does not exist")
    return delete_user
