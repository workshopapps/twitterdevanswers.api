from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database, schema, model, utils, oauth

router = APIRouter(
    prefix='/auth',
    tags=['Authentication'])

@router.post('/signin', )
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()

    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalide Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalide Credentials")

    access_token = oauth.create_access_token(data={'user_id':user.user_id}
    )

    return {'success' : True, 'Message': 'user signed in successfully ', 
            'data': {
                        'userName': user.username,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'email' :user.email,
                        'imageUrl': user.imageUrl
        },
        'token' : access_token
        }
     
@router.post('/signup', status_code=status.HTTP_201_CREATED)
def user_signnup(user_credentials: schema.UserSignInRequest, db: Session = Depends(database.get_db)):
    user_credentials.password = utils.hash(user_credentials.password)
    new_user = model.User(**user_credentials.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    access_token = oauth.create_access_token(data={'user_id':user.user_id })
    return {
        'Success': True,
        'Message':'user added successfully',
        'data':
        {
        'userName': user_credentials.username,
        'firstName': user_credentials.firstname,
        'lastName':user_credentials.lastname,
        'email': user_credentials.email,
        'imageUrl': user_credentials.imageURL
        },
'Token' : access_token}

@router.patch('/change-password')
def change_password(update_password: schema.ChangePasswordRequest, db: Session = Depends(database.get_db),current_user: int = Depends(oauth.get_current_user)):
    user = db.query(model.User).filter(model.User.user_id == current_user).first()
    if user.id is None: 
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user.id} does not exit")
    if user.id != current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You are not authorised to perform the required action")
    user.password = update_password.newPassword
    db.commit()
    return {'sucess': True, 'message': 'Password Changed'}



