import schema
import crud
from database import get_db
from model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request


router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ List all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{user_id}', response_model=schema.User)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    """ Get a user by it's user_id  """

    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status=404, detail=f" user with user_id : {user_id} not found")
    return {"success": True, 'data': user}

# @router.post("/")
# def create_user(user:schema.User, db: Session = Depends(get_db)):
#     """Create a user"""
#     new_user = model.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh()
#     return new_user

@router.delete("/{user_id}")
def delete_user(db: Session = Depends(get_db)):
    """ delete a user by it's user_id  """
    data =crud.delete_user(db, user_id=user_id)
    return data

@router.put("/{user_id}")
def update_user(user:schema.UserUpdate, db: Session = Depends(get_db)):
    """update a user"""
    user = crud.update_user(db, user, user_id=user_id)
    return user
