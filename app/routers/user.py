import sys
sys.path.append('..')
from app import schema
from app import crud
from database import get_db
from model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from oauth import get_current_user
import model


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{username}')
def fetch_user(username: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Fetch a user by username  """

    user = crud.get_user(db, username=username)
    if not user:
        raise HTTPException(
            status=404, detail=f" User {username} not found")
    return {"success": True, 'data': user}


@router.patch('/edit/{username}')
def update_user(user: schema.UserUpdate, username: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Update a User profile by username  """

    user_db = db.query(User).filter(User.username == username).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_db.username == current_user.username:
        update_user = db.query(model.User).filter(
            model.User.username == username).first()
        if update_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        if isinstance(user, dict):
            update_data = user
        else:
            update_data = user.dict(exclude_unset=True)
        for field in update_data:
            setattr(update_user, field, update_data[field])

        db.add(update_user)
        db.commit()
        db.refresh(update_user)
        return {"success": True,"message": "Profile Updated","data": update_data}

        

@router.delete('/delete/{username}')
def delete_user(username: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Delete a user by username  """

    delete_user = crud.delete_user(db, username=username)
    if not delete_user:
        raise HTTPException(
            status=404, detail=f" User {username} does not exist")
    return delete_user
