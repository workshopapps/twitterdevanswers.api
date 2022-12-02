import sys
sys.path.append('..')
from app import schema
from app import crud
from app.database import get_db
from app.model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from app.oauth import get_current_user
from app import model


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{user_id}')
def fetch_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Fetch a user by it's user_id  """

    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status=404, detail=f" user with user_id : {user_id} not found")
    return {"success": True, 'data': user}


@router.patch('/edit/{user_id}', response_model=schema.UserUpdate)
def update_user(user: schema.UserUpdate, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Update a User profile by user_id  """

    user_db = db.query(User).filter(User.user_id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_db.user_id == current_user.user_id:
        update_user = db.query(model.User).filter(
            model.User.user_id == user_id).first()

        if update_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # update_data = user.dict(exclude_unset=True)
        if isinstance(user, dict):
            update_data = user
        else:
            update_data = user.dict(exclude_unset=True)
        for field in update_data:
            setattr(update_user, field, update_data[field])
        # print(update_data)
        # for key, value in update_data.items():
        #     setattr(update_data, key, value)
        db.add(update_user)
        db.commit()
        db.refresh(update_user)
        return {"success": True, "message": "Profile Updated", "data": update_user}


@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Delete a user by it's user_id  """

    delete_user = crud.delete_user(db, user_id=user_id)
    if not delete_user:
        raise HTTPException(
            status=404, detail=f"user with user_id : {user_id} does not exist")
    return delete_user
