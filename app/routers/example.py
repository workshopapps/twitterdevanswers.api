from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import model, schema, utils 
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)
# This is an example of how u can use the schema created to parse data sent and also structure your reponse 
#Also this is how you incorporate our database into ur enpoint --> db : Session = Depends(get_db) 
# Then work with Database like this as shown below 
#This is just like a demo incase you are stuck 

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_users(user : schema.UserCreate, db : Session = Depends(get_db)):
    
    user.password = utils.hash(user.password)
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user 
