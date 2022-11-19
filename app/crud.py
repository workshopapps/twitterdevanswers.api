from sqlalchemy.orm import Session
import model, schema

# create user
def create_user(db: Session, user: schema.CreateUser):
    user_password = utils.hash(user.password)
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#  get a user
def get_user(db: Session, user_id: int):
    user = db.query(model.User).filter(model.User.id == user_id).first()
    return user

#  get all users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(model.User).offset(skip).limit(limit).all()
    return { "success":True, 'data':users }

# Update a user 
def update_user(db: Session, user_id: int,user: schema.UserUpdate):
    update_user = db.query(models.User).filter(models.User.user_id == user_id).first() 

    if not update_user :
        raise HTTPException(status_code=404, detail="User not found")
    for key,value in update_user.items():
        setattr(db, key, value)
        db.add( update_user)
        db.commit()
        db.refresh( update_user)
    return {"success":True,"message": "Profile Updated","data":update_user}

# Delete a user
def delete_user(db: Session,user_id:int):
    delete_user = db.query(model.User).filter(model.User.id ==user_id).first()
    db.delete(user)
    db.commit()
    db.refresh(user)
    return {"success":True,"message":"profile removed"}
    

