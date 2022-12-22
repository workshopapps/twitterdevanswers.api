from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from app.config import settings
import pyotp
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import yagmail
from app.oauth import get_current_user, verify_access_token, create_access_token, authenticate_user
from datetime import timedelta
from app.model import Wallet
from app import database, schema, model, utils, oauth
from uuid import uuid4

app_passwd = settings.app_passwd
app_email = settings.app_email

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


# send reset email
def send_reset_mail(email, token):
    msg = f'''
		   To reset your password visit the following link:
			{token}
			If you did not make this request then simply ignore this email) '''

    with yagmail.SMTP(app_email, app_passwd) as yag:
        yag.send(to=email, subject='Passowrd Reset Request', contents=msg)


def send_signup_mail(email, token):
    msg = f''' 
           To Sign up on DevAsk, use this code to verify your email :
            {token}   
            
            If you did not make this request, Simply ignore this email '''

    with yagmail.SMTP(app_email, app_passwd) as yag:
        yag.send(to=email, subject='DevAsk Email Verification', contents=msg)


@router.post('/signin')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.is_verified == True:
        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires)

        return {
            "data": {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "name": user.first_name + user.last_name
            },
            "access_token": access_token,
            "token_type": "bearer"}
    return HTTPException(status_code=401, detail="Verify your email to login")


totp = ''


@router.post('/send_email_code', status_code=status.HTTP_200_OK)
def user_signnup(request: schema.Email):
    global totp
    secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(secret_key, interval=600)
    send_signup_mail(request.email, totp.now())
    return {"msg": "email sent"}


def auth_otp(code):

    return totp.verify(code)


@router.post('/signup', status_code=status.HTTP_201_CREATED)
def user_signnup(user_credentials: schema.UserSignInRequest, db: Session = Depends(database.get_db)):
    user_credentials.password = utils.hash(user_credentials.password)
    user = db.query(model.User).filter(
        model.User.email == user_credentials.email).first()

    if user:
        return HTTPException(status_code=400, detail={"msg": "User already exists"})

    new_user = model.User(username=user_credentials.username,
                          firstname = user_credentials.firstname,
                          lastname = user_credentials.lastname,
                          email=user_credentials.email,
                          password=user_credentials.password,

                          )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # creating User Wallet
    wallet_id = uuid4()
    wallet_obj = Wallet(user_id=new_user.user_id, id=wallet_id)
    db.add(wallet_obj)
    db.commit()
    db.refresh(wallet_obj)

    user = db.query(model.User).filter(
        model.User.email == user_credentials.email).first()
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {
        'Success': True,
        'Message': 'user added successfully',
        'data':
            {
                'user_id': user.user_id,
                'userName': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'wallet': wallet_obj
            },
        'Token': access_token,
        'Token_type': 'Bearer'}


@router.post('/verify-email', status_code=status.HTTP_202_ACCEPTED)
def verify_email(credentials: schema.UserVerification, db: Session = Depends(database.get_db)):
    if auth_otp(code=credentials.verification_code):
        user = db.query(model.User).filter(
            model.User.email == credentials.email)
        if user:
            user.update({'is_verified': True})
            db.commit()
            return {"success": True, "msg": "Email verified"}
        else:
            return HTTPException(status_code=404, detail="User with the current email doesn't exists")
    else:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED,
                            detail="OTP is either a wrong one or has expired ")


@router.post('/admin-signup', status_code=status.HTTP_201_CREATED)
def admin_signnup(user_credentials: schema.UserSignInAdminRequest, db: Session = Depends(database.get_db)):
    user_credentials.password = utils.hash(user_credentials.password)
    user = db.query(model.User).filter(
        model.User.email == user_credentials.email).first()
    if user:
        return HTTPException(status_code=400, detail={"msg": "User already exists"})

    new_user = model.User(username=user_credentials.username,
                          firstname = user_credentials.firstname,
                          lastname = user_credentials.lastname,  
                          email=user_credentials.email,
                          password=user_credentials.password,
                          is_admin=True
                          )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # creating User Wallet
    wallet_id = uuid4()
    wallet_obj = Wallet(user_id=new_user.user_id, id=wallet_id)
    db.add(wallet_obj)
    db.commit()
    db.refresh(wallet_obj)

    user = db.query(model.User).filter(
        model.User.email == user_credentials.email).first()
    access_token = oauth.create_access_token(
        data={'user_id': user.user_id})
    return {
        'Success': True,
        'Message': 'user added successfully',
        'data':
            {
                'user_id': user.user_id,
                'userName': user.username,
                'firstname': user.first_name,
                'lastname': user.last_name,
                'email': user.email,
                'wallet': wallet_obj
            },
        'Token': access_token}


@router.put('/change-password', )
def change_password(update_password: schema.ChangePasswordRequest, db: Session = Depends(database.get_db), current_user: int = Depends(get_current_user)):
    print(current_user)
    user_query = db.query(model.User).filter(
        model.User.user_id == current_user.user_id)

    user = user_query.first()
    if not utils.verify_password(update_password.oldPassword, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Wrong Old Password ")
    if user.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not authorised to perform the required action")
    updated_password = utils.hash(update_password.newPassword)

    user_query.update({'password': str(updated_password)},
                      synchronize_session=False)
    db.commit()
    return {'sucess': True, 'message': 'Password Changed'}


@router.post('/forget-password')
def forget_password(email: schema.Email, request: Request, db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == email.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with email: {email.email} does not exit")

    token = oauth.create_access_token({'user_id': user.user_id})
    url = "https://devask.hng.tech/#/password-recovery/" + token

    send_reset_mail(user.email, url)

    return {'success': True, 'message': 'token sent to provided email'}


@router.put('/forget-password/{token}')
def verify_password_token(token: str,  password: schema.ForgotPassword, db: Session = Depends(database.get_db)):
    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"The token is invalid or has expired")
    user_query = db.query(model.User).filter(model.User.user_id == user_id)
    user = user_query.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This user does not exist")
    new_password = utils.hash(password.newPassword)
    user_query.update({'password': new_password}, synchronize_session=False)
    db.commit()

    return {'sucess': True, 'Message': f'User {user.email}  password has been updated '}


@router.put('/setup-mfa')
def two_factor_auth(two_factor: schema.Email, db: Session = Depends(database.get_db), current_user=Depends(get_current_user)):
    user_query = db.query(model.User).filter(
        model.User.email == two_factor.email)
    user = user_query.first()
    if user.mfa_hash:
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED, detail='MFA already setup')
    mfa_hash = pyotp.random_base32()
    enable_2fa = user_query.update(
        {'mfa_hash': mfa_hash}, synchronize_session=False)
    db.commit()

    return {'message': 'MFA Setup Successfully'}


@router.post('/send-mfa')
def send_mfa(email: schema.Email, db: Session = Depends(database.get_db), current_user=Depends(get_current_user)):

    user = db.query(model.User).filter(model.User.email == email.email).first()
    uri = pyotp.totp.TOTP(user.mfa_hash).provisioning_uri(
        user.email, issuer_name="Dev Ask")
    qrcode_uri = "https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl={}".format(
        uri)

    return {'qr_code': qrcode_uri}


def verify_wallet_otp(user_mfa, code):
    walletOtp = pyotp.TOTP(user_mfa)
    return walletOtp.verify(code)


@router.post('/validate-mfa')
def validate_otp(otp: schema.two_factor, db: Session = Depends(database.get_db), current_user=Depends(get_current_user)):
    user = db.query(model.User).filter(model.User.email == otp.email).first()
    user_mfa = user.mfa_hash
    if not user.mfa_hash:
        return {'message': 'User has not enabled 2FA'}
    if user != current_user:
        return {'Messaage': ' This user is not the right '}

    if verify_wallet_otp(user_mfa, otp.mfa_hash):
        return {'Success': True}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Wrong 2FA')
