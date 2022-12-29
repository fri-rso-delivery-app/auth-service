from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.config import Settings, get_settings

from app.models.jwt import *
from app.auth import authenticate_user, create_access_token


router = APIRouter(
    prefix='/jwt',
    tags=['jwt'],
)


@router.post('/token', response_model=JWToken)
async def get_token(*,
    form_data: OAuth2PasswordRequestForm = Depends(),
    settings: Settings = Depends(get_settings),
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=settings.api_token_expire_min)
    access_token = create_access_token(
        data={ 'sub': user.username, 'user_id': str(user.id)},
        expires_delta=access_token_expires
    )

    return JWToken(
        access_token=access_token,
        token_type='bearer',
    )
