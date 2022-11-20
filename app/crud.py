from sqlalchemy.orm import Session
from . import model
from . import schema
from fastapi.exceptions import HTTPException


#  get a user
def get_user(db: Session, user_id: int):
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    return user


#  get all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(model.User).offset(skip).limit(limit).all()
    return {"success": True, 'data': users}


# Update a user
def update_user(db: Session, user_id: int, user: schema.UserUpdate):
    update_user = db.query(model.User).filter(
        model.User.user_id == user_id)
    updated_user = update_user.first(0)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    update_user.filter(model.User.user_id == user_id).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(updated_user)
    return {"success": True, "message": "Profile Updated", "data": updated_user}


# Delete a user
def delete_user(db: Session, user_id: int):
    delete_user = db.query(model.User).filter(
        model.User.user_id == user_id).first()
    if delete_user:
        db.delete(delete_user)
        db.commit()
        return {"success": True, "message": "profile removed"}
    else:
        return {"success": False, "message": "User does not exist"}
