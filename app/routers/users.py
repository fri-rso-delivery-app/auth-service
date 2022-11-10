from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from app.db import db
from app.models.users import *


TABLE = 'users'
table = db[TABLE]


router = APIRouter(
    prefix='/users',
    tags=['users'],
)


async def get_user(id: str) -> User:
    user = await table.find_one({'_id': id})
    if not user: raise HTTPException(status_code=404, detail=f'User not found')

    return User(**user)


async def check_username_taken(username: str):
    user = await table.find_one({'username': username})
    if user: raise HTTPException(status_code=400, detail=f'username taken')

async def check_email_taken(email: str):
    user = await table.find_one({'email': email})
    if user: raise HTTPException(status_code=400, detail=f'email taken')


@router.post('/', response_model=UserRead)
async def create_user(user: UserCreate):
    # checks
    await check_username_taken(user.username)
    await check_email_taken(user.email)

    # create
    user_db = jsonable_encoder(User(**user.dict()))
    new_user = await table.insert_one(user_db)
    created_user = await table.find_one({'_id': new_user.inserted_id})
    
    return created_user


@router.get('/', response_model=List[UserRead])
async def list_users():
    return await table.find().to_list(1000)


@router.get('/{id}', response_model=UserRead)
async def read_user(user: User = Depends(get_user)):
    return user


@router.patch('/{id}', response_model=UserRead)
async def update_user(*,
    user: User = Depends(get_user),
    user_update: UserUpdate
):
    # checks
    if user.username: await check_username_taken(user.username)
    if user.email: await check_email_taken(user.email)

    # update user
    user_update = user_update.dict(exclude_unset=True)
    update_result = await table.update_one({'_id': str(user.id)}, {'$set': user_update})
    if update_result.modified_count == 1:
        user_db = await table.find_one({'_id': str(user.id)})

    return user_db


@router.delete('/{id}')
async def delete_user(user: User = Depends(get_user)):
    await table.delete_one({'_id': str(user.id)})

    return { 'ok': True }
