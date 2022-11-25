from sqlalchemy.orm import Session
from . import model,schema
from fastapi.exceptions import HTTPException


def get_user(db: Session, user_id: int):
    
    """ Get a user from the database based on their id  """

    user = db.query(model.User).filter(model.User.user_id == user_id).first()  
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    
    """ Get all users in the database  """     
    
    users = db.query(model.User).offset(skip).limit(limit).all()
    return {"success": True, 'data': users}


def update_user(db: Session, user_id: int, user: schema.UserUpdate):
   
    """ Update a User profile """

    update_user = db.query(model.User).filter(
        model.User.user_id == user_id).first()

    if  update_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user.dict(exclude_unset=True)
    update_user.filter(model.User.user_id == user_id).update(
        update_data, synchronize_session=False)
    db.commit()
    db.refresh(update_user)
    return {"success": True, "message": "Profile Updated", "data": update_user}


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
