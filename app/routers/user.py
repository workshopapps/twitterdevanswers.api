import sys
sys.path.append('..')
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from typing import List
from app.model import *
from app.database import get_db
from app import crud
from app import schema


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
   
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{user_id}')
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    
    """ Fetch a user by it's user_id  """
  
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status=404, detail=f" user with user_id : {user_id} not found")
    return {"success": True, 'data': user}


@router.patch('/edit/{user_id}', response_model=schema.UserUpdate)
def update_user(user: schema.UserUpdate, user_id: int, db: Session = Depends(get_db)):
    
    """ Update a User profile by user_id  """
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, user=user, user_id=user_id)


@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    
    """ Delete a user by it's user_id  """
  
    delete_user = crud.delete_user(db, user_id=user_id)
    if not delete_user:
        raise HTTPException(
            status=404, detail=f"user with user_id : {user_id} does not exist")
    return delete_user
