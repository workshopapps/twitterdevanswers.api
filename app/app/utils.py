from passlib.context import CryptContext
import yagmail
pwd_context = CryptContext(schemes=['bcrypt'], deprecated= "auto")

def hash(password):
    return pwd_context.hash(password)

def verify(plain_passwd, hashed_passwd):
    return pwd_context.verify(plain_passwd, hashed_passwd)


