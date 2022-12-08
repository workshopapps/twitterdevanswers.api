import sys
sys.path.append('..')
from app import model
from app.oauth import get_current_user, get_admin
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from typing import List
from app.model import *
from app.database import get_db
from app import crud, schema



router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/')
def fetch_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{username}')
def fetch_user(username: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """ Fetch a user by username  """

    user = crud.get_user(db, username=username)
    if not user:
        raise HTTPException(
            status_code=404, detail=f" User {username} not found")
    return {"success": True, 'data': user}


@router.patch('/edit/{username}')
def update_user(user: schema.UserUpdate, username: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
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


@router.delete('/delete/{username}/{user_id}')
def delete_user(username: str, user_id: int, db: Session = Depends(get_db),current_user = Depends(get_current_user) ):
    """ Delete a user by it's username  """
   
    if user_id == current_user.user_id or current_user.is_admin:
        try:
            delete_user = crud.delete_user(
                db, username=username, current_user=user_id)
            if not delete_user:
                raise HTTPException(
                    status_code=404, detail=f"user with user_id : {username} does not exist")
            return {"success": True, "data": "User has been deleted successfully"}
        except:

            return {"error" : "Unable to delete user"}



@router.get("/remove-admin/{user_id}")
def remove_admin(usernname:int, db: Session = Depends(get_db), admin = Depends(get_admin)):
    user = db.query(model.User).filter(model.User.username == usernname).update({'is_admin': False})
    return {'Success': True, "Details" : "User deactivated as admin "}

@router.get("/make-admin/{user_id}")
def remove_admin(usernname:int, db: Session = Depends(get_db), admin = Depends(get_admin)):
    try:
        user = db.query(model.User).filter(model.User.username == usernname).update({'is_admin': True})
        return {'Success': True, "Details" : "User deactivated as admin "}
    except:
        raise HTTPException(
                status_code=405, detail=f"An error occured pls try again ")