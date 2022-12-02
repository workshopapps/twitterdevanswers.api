from sqlalchemy.orm import Session
from . import model, schema
from fastapi.exceptions import HTTPException


def get_user(db: Session, user_id: int):
    """ Get a user from the database based on their id  """

    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    return {
        "user_id": user.user_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "description": user.description,
        "image_url": user.image_url,
        "location": user.location,
        "account_balance": user.account_balance
    }


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """ Get all users in the database  """

    users = db.query(model.User).offset(skip).limit(limit).all()
    users_list = []
    for user in users:
        users_list.append({
            "user_id": user.user_id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "description": user.description,
            "image_url": user.image_url,
            "location": user.location,
            "account_balance": user.account_balance
        })
    return {"success": True, 'data': users_list}


def delete_user(db: Session, user_id: int):
    """ Delete a user Profile  """

    delete_user = db.query(model.User).filter(
        model.User.user_id == user_id).first()
    if delete_user:
        db.delete(delete_user)
        db.commit()
        return {"success": True, "message": "profile removed"}
    else:
        return {"success": False, "message": "User does not exist"}
