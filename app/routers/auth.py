from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.config import settings
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session  
import yagmail

from app import database, schema, model, utils, oauth

app_passwd = settings.app_passwd
app_email = settings.app_email

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post('/signin')
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(
        model.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth.create_access_token(data={'user_id': user.user_id}
                                             )

    return {'success': True, 'Message': 'user signed in successfully ',
            'data': {
                'user_id' : user.user_id,
                'userName': user.username,
                'email': user.email,
            },
            'token': access_token
            }


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def user_signnup(user_credentials: schema.UserSignInRequest, db: Session = Depends(database.get_db)):
    user_credentials.password = utils.hash(user_credentials.password)
    user = db.query(model.User).filter(
        model.User.email == user_credentials.email).first()
    if user:
        return HTTPException(status_code=400, detail={"msg": "User already exists"})
    new_user = model.User( username = user_credentials.username, 
                                email = user_credentials.email, 
                                password = user_credentials.password, 
                                )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user = db.query(model.User).filter(
        model.User.email == user_credentials.email).first()
    access_token = oauth.create_access_token(data={'user_id': user.user_id})
    return {
        'Success': True,
        'Message': 'user added successfully',
        'data':
        {
            'user_id' : user.user_id,
            'userName': user.username,
            'email': user.email,
        },
        'Token': access_token}


@router.put('/change-password')
def change_password(update_password: schema.ChangePasswordRequest, db: Session = Depends(database.get_db), current_user: int = Depends(oauth.get_current_user)):
    print(current_user)
    user_query = db.query(model.User).filter(model.User.user_id == current_user.user_id)
    
    user = user_query.first()
    print(current_user)
    if user.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorised to perform the required action")
    updated_password = utils.hash(update_password.newPassword)
    
    user_query.update({'password': str(updated_password)}, synchronize_session=False)
    db.commit()
    return {'sucess': True, 'message': 'Password Changed'}


@router.post('/forget-password', name='getPass')
def forget_password(email: schema.Email, request : Request,db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == email.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {email.email} does not exit")

    token = oauth.create_access_token({'user_id': user.user_id})
    url = request.url._url+'/' + token

    send_reset_mail(user.email, url)

    return {'success': True, 'message': 'token sent to provided email'}


@router.post('/forget-password/{token}')
def verify_password_token(token: str,  password: schema.ForgotPassword, db: Session = Depends(database.get_db),):

    user_id = oauth.verify_access_token(token)
    user = db.query(model.User).filter(model.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Check token again")
    user.password = utils.hash(password.newPassword)
    db.commit()

    return {'success': True, 'message': 'Password Changed'}

def send_reset_mail(user, url):
    
    msg = f''' 
           To reset your password visit the following link:
            {url}  
            If you did not make this request then simply ignore this email) '''
    with yagmail.SMTP(app_email,app_passwd) as yag:
        yag.send(to=user, subject='Passowrd Reset Request', contents=msg)