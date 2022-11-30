from sqlalchemy.orm import Session
from . import model,schema
from fastapi.exceptions import HTTPException

def get_user(db: Session, username: str):
    
    """ Get a user from the database based on their id  """

    user = db.query(model.User).filter(model.User.username == username).first()
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    
    """ Get all users in the database  """     
    
    users = db.query(model.User).offset(skip).limit(limit).all()
    return {"success": True, 'data': users}


def update_user(db: Session, username: str, user: schema.UserUpdate):
   
    """ Update a User profile """

    update_user = db.query(model.User).filter(
        model.User.username == username).first()

    if update_user:
        update_user.username = user.username
        update_user.first_name = user.first_name
        update_user.last_name = user.last_name
        update_user.description= user.description
        update_user.role = user.role
        update_user.position = user.position
        update_user.image_url = user.image_url
        update_user.phone_number = user.phone_number
        update_user.location = user.location
        update_user.stack = user.stacks
        update_user.link = user.links

    db.commit()
    db.refresh(update_user)

    return {"success": True,
            "message": "Profile Updated",
            "data": {
                'username':update_user.username,
                'firstname':update_user.first_name,
                'last_name':update_user.last_name,
                'description':update_user.description,
                'role':update_user.role,
                'position':update_user.position,
                'image_url':update_user.image_url,
                'phone_number':update_user.phone_number,
                'location':update_user.location,
                'stacks':update_user.stack,
                'links':update_user.links
            }
      }

# Things to be added :-
# stack , position ,role,acct_balance,phone_no , links
# wallet_id , user_id , 
# use update 
# all endpoints work with authorization
# tags to be added to questions

# internal server error (questions)
# auth,users,questions
# 

def delete_user(db: Session, user_id: int):
    
    """ Delete a user Profile  """

    delete_user = db.query(model.User).filter(
        model.User.user_id == user_id).first()

    db.delete(delete_user)
    db.commit()
    return{"sucess":True,"message":"Profile successfully removed"} 