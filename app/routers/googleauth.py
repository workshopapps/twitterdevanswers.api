import os
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from main import app
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import Request, Depends, APIRouter
from starlette.responses import RedirectResponse
from model import User
from database import get_db
from sqlalchemy.orm import Session
from oauth import create_access_token
from config import settings
from datetime import timedelta


# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Auth
router = APIRouter('google-auth', prefix='/google-auth')


# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
router.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


@ router.route('/login')
async def login(request: Request):
    # This creates the url for the /auth endpoint
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@ router.route('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url='/')
    user_data = await oauth.google.parse_id_token(request, access_token)
    user = db.query(User).filter(User.email == user_data["email"]).first()
    if user:
        access_token_expires = timedelta(
            minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires)

    return {"access_token": access_token,
            "data": {
                "user_id": user.user_id,
                "usename": user.username,
                "email": user.email,
                "name": user.first_name + user.last_name
            },
            "token_type": "bearer"}
