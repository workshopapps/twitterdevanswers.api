from fastapi import FastAPI ,Depends, HTTPException , APIRouter
from sqlmodel import Session
from typing import List
from models import *


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


# Create/Add a User
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schema.ReadUser)
def create_user(user:schema.CreateUser , db:Session = Depends(get_db)):
    #  Get new Users mail
    new_user = db.query(models.User).filter(models.User.email == email).first()    
    # check if user is already registered
    if new_user:
        raise HTTPException(status_code=400, detail= " User has already been created")
    return crud.create_user(db, user=user)


# Get all users
@router.get('/',response_model=list[schema.UserSignInRequest])   
def fetch_users(skip: int = 0,limit: int = 100,db: Session = Depends(get_db)):
    return crud.get_users(db,skip=skip,limit=limit)


# Get a User  
@router.get('/{user_id}')
def fetch_user(user_id:int,db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException( status = 404 , detail = f" user with user_id : {user_id} not found")
    return{"success":True,'data':user}


# update a user
@router.patch('/{user_id}',response_model =ReadUser)      
def update_user(user:UserUpdate,user_id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first() 
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")            
    return crud.update_user(db,user=user,user_id=user_id)   

# delete a user
@router.delete('/{user_id}')   
def delete_user(user_id:int, db: Session = Depends(get_db)):
    delete_user = crud.delete_user(db, user_id=user_id)
    if not delete_user:
        raise HTTPException( status = 404 , detail = f"user with user_id : {user_id} does not exist")  
    return delete_user


