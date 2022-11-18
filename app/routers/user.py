from fastapi import FastAPI ,Depends, HTTPException , APIRouter
from sqlmodel import Session
from typing import List
from models import *


router = APIRouter()

# Create/Add a User
@router.post('/user/',response_model=ReadUser)
def create_user(new_user:CreateUser):
    with Session(engine) as session:
        db = User.from_orm(new_user)
        session.add(new_user)
        print('commiting....')
        session.commit()
        print('commited :)')
        session.refresh()
        return {"success":True,"data":new_user}

# Get all users
@router.get('/users')   
def fetch_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return { "success":True, 'data':user }
  

# Get a User  
@router.get('/user/{user_id}')
def fetch_a_user(user_id:int):
     with Session(engine) as session:
        if user:
             user = session.get(User,user_id)
        raise HTTPException( status = 404 , detail = f" user with user_id : {user_id} not found")
        return{"success":True,'data':user}

# update a user
@router.patch('/user/update/{user_id}',response_model =ReadUser)      
def update_user(user_update:UserUpdate,user_id:int):
    with Session(engine) as session :
        db = session.get(User,user_id)
        if not db :
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user_update.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db, key, value)
        session.add(db)
        session.commit()
        session.refresh(db)
        return {"success":True,"message": "Profile Updated","data": db}


# delete a user
@router.delete('/user/del/{user_id}')   
def delete_user(user_id:int):
     with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException( status = 404 , detail = f"user with user_id : {user_id} does not exist")  
        session.delete(user)
        session.commit()
        return { "sucess" : True , "message" : "profile removed"}

