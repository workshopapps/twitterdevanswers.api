from app import crud, schema
from app.database import get_db
from app.model import *
from typing import List
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from app.oauth import get_current_user
from app import model
import sys
sys.path.append('..')


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{user_id}')
def fetch_user_id(user_id: int, db: Session = Depends(get_db), urrent_user: int = Depends(get_current_user)):
    """ Fetch a user by Id  """

    user = crud.get_user_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f" User {user_id} not found")
    return {"success": True, 'data': user}


@router.get('/{username}')
def fetch_user(username: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Fetch a user by username  """

    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=404, detail=f" User {username} not found")
    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth,
        "gender": user.gender,
        "description": user.description,
        "phone_number": user.phone_number,
        "work_experience": user.work_experience,
        "position": user.position,
        "stack": user.stack,
        "links": [user.links],
        "role": user.role,
        "image_url": user.image_url,
        "location": user.location,
        "is_admin": user.is_admin,
        "account_balance": user.account_balance,
        "followers": user.followers,
        "following": user.following,
        "date_joined": user.created_at
    }
    return {"success": True, 'data': user_data}


@router.patch('/edit/{username}')
def update_user(user: schema.UserUpdate, username: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
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
        return {"success": True, "message": "Profile Updated", "data": update_data}
    else:
        return {"success": False, "message":  "You're not authorized to perform this update "}


@router.delete('/delete/{username}')
def delete_user(username: str, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """ Delete a user by username  """
    delete_user = crud.delete_user(
        db, username=username, current_user=current_user)
    if not delete_user:
        raise HTTPException(
            status=404, detail=f" User {username} does not exist")
    return delete_user
