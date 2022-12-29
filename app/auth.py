from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

from app import config
from app.db import db
from app.models.jwt import *
from app.models.users import *

from app.config import Settings, get_settings


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# auth scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'jwt/token')


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

users_table = db['users']

async def authenticate_user(username: str, password: str):
    # check username
    user = await users_table.find_one({'username': username})
    if not user: return False

    # convert to obj
    user = User(**user)
    # verify
    if not verify_password(password, user.password_hash): return False

    return user

def create_access_token(
    data: dict, expires_delta: timedelta | None = None,
):
    # get settings
    settings = get_settings()

    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.api_secret_key, algorithm=settings.api_jwt_algorithm)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    # generate exteption to re-use
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    # verify user credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('user_id')
        if username is None or user_id is None:
            raise credentials_exception
        
        return JWTokenData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    # finally (this part of the code should be unreachable)
    raise credentials_exception
