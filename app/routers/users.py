from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.models.users import *
from app.models.jwt import *
from app.auth import get_password_hash, get_current_user


TABLE = 'users'
table = db[TABLE]


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


async def get_user(id: str) -> User:
    user = await table.find_one({'_id': str(id)})
    if not user: raise HTTPException(status_code=404, detail=f'User not found')

    return User(**user)


async def check_username_taken(username: str):
    user = await table.find_one({'username': username})
    if user: raise HTTPException(status_code=400, detail=f'username taken')

async def check_email_taken(email: str):
    user = await table.find_one({'email': email})
    if user: raise HTTPException(status_code=400, detail=f'email taken')


@router.post('/register', response_model=UserRead)
async def register_user(user: UserCreate, password: str):
    # checks
    await check_username_taken(user.username)
    await check_email_taken(user.email)

    # create
    user_db = jsonable_encoder(User(
        **user.dict(),
        password_hash=get_password_hash(password)
    ))
    new_user = await table.insert_one(user_db)
    created_user = await table.find_one({'_id': new_user.inserted_id})
    
    return created_user


# do not enable
#@router.get('/', response_model=List[UserRead])
#async def list_users():
#    return await table.find().to_list(1000)
#
#
#@router.get('/{id}', response_model=UserRead)
#async def read_user(user: User = Depends(get_user)):
#    return user

@router.get('/my_profile', response_model=UserRead)
async def read_user(token: JWTokenData = Depends(get_current_user)):
    return await get_user(token.user_id)


@router.patch('/my_profile', response_model=UserRead)
async def update_user(*,
    token: JWTokenData = Depends(get_current_user),
    user_update: UserUpdate
):
    # checks
    if user_update.email: await check_email_taken(user_update.email)

    # update user
    user_update = user_update.dict(exclude_unset=True)
    await table.update_one({'_id': str(token.user_id)}, {'$set': user_update})
    
    return await get_user(str(token.user_id))


@router.delete('/my_profile')
async def delete_user(token: JWTokenData = Depends(get_current_user)):
    await table.delete_one({'_id': str(token.user_id)})

    return { 'ok': True }
