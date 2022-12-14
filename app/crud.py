from sqlalchemy.orm import Session
from app import model, schema
from fastapi.exceptions import HTTPException


def get_user(db: Session, username: str):
    """ Get a user from the database based on their Username  """

    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        return None
    return {
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


def get_user_id(db: Session, user_id: int):
    """ Get a user from the database based on their id  """

    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user is None:
        return None
    return {
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


def get_user_username(db: Session, username: str):
    """ Get a user from the database based on their id  """

    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        return None
    return {
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
        })
    return {"success": True, 'data': users_list}


def delete_user(db: Session, username: str, current_user: int):
    """ Delete a user Profile  """

    delete_user = db.query(model.User).filter(
        model.User.username == username).first()
    if delete_user:
        wallet = db.query(model.Wallet).filter(
            model.Wallet.user_id == delete_user.user_id).first()
        if delete_user.user_id == current_user.user_id or current_user.is_admin == True:
            db.delete(wallet)
            db.commit()
            db.delete(delete_user)
            db.commit()
            return {"success": True, "message": "profile removed"}
        else:
            return {"success": False, "message": "You're not authorized to perform this operation"}
    else:
        return {"success": False, "message": "User does not exist"}
