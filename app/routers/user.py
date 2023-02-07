from fastapi import FastAPI,status, Depends, HTTPException, APIRouter, Request
from app import crud, schema
from app.database import get_db
from app.model import *
from app import model
from typing import List
from sqlalchemy.orm import Session
from app.oauth import get_current_user
import sys
sys.path.append('..')


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.get('/',status_code=status.HTTP_200_OK)
def fetch_users( skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ List to get all users """

    return crud.get_users(db, skip=skip, limit=limit)


@router.get('/{user_id}',status_code=status.HTTP_200_OK)
def fetch_user_id(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Fetch a user by Id  """

    user = crud.get_user_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail=f" User {user_id} not found")
    return {"success": True, 'data': user}


@router.get('/get/{username}',status_code=status.HTTP_200_OK)
def fetch_by_username(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Fetches user by username"""
    user = db.query(model.User).filter(
        model.User.username == username).first()
    if user:
        user_data = crud.get_user(db, username)
        return {"success": True, 'data': user_data}
    return HTTPException(status_code=404, detail="Username doesn't exist.")


@router.get('/likes/{user_id}',status_code=status.HTTP_200_OK)
def fetch_user_likes(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Fetch user likes"""
    likes = db.query(model.Like).filter(model.Like.user_id == user_id).all()
    if likes:
        return {"total_likes": len(likes)}
    else:
        return HTTPException(status_code=404, detail="User hasn't liked any post yet")


@router.get('/rewards/{user_id}',status_code=status.HTTP_200_OK)
def fetch_user_rewards(user_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Fetch user total earned rewards"""
    tokens_on_signup = 100
    reward = db.query(model.Wallet).filter(
        model.Wallet.user_id == user_id).first()
    if reward:
        return {"success":True,"data":{"reward_on_signup":tokens_on_signup,"earnings":reward.total_earned,"total_earnings": reward.total_earned + tokens_on_signup}}
    else:
        return HTTPException(status_code=404, detail="User not found")
        

@router.patch('/edit/{username}',status_code=status.HTTP_200_OK)
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


@router.patch('/update/{user_id}',status_code=status.HTTP_200_OK)
def update_user_id(user: schema.UserUpdate, user_id: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """ Update a User profile by user_id  """

    user_db = db.query(User).filter(User.user_id == user_id).first()
    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_db.user_id == current_user.user_id:
        update_user = db.query(model.User).filter(
            model.User.user_id == user_id).first()
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


@router.delete('/delete/{username}',status_code=status.HTTP_200_OK)
def delete_user(username: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    """ Delete a user by username  """
    delete_user = crud.delete_user(
        db, username=username, current_user=current_user)
    if not delete_user:
        raise HTTPException(
            status=404, detail=f" User {username} does not exist")
    return delete_user


