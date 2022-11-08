from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI(
    title='Authentication microservice',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# autocreate tables (use migrations instead)
#@app.on_event("startup")
#def on_startup():
#    db.create_db_and_tables()

# auth router
#from app.routers.auth import auth
#app.include_router(auth.router)


#@app.get("/", response_class=HTMLResponse)
#async def root(request: Request):
#    return f"""
#        <h1> Hello! Docs available at <a href="{request.scope.get("root_path")}/docs">{request.scope.get("root_path")}/docs</a> </h1>
#    """


from .db import db
from .models import *

TABLE = 'users'
table = db[TABLE]

@app.post('/', response_model=User)
async def create_user(user: UserCreate):
    user_db = jsonable_encoder(User(**user.dict()))

    new_user = await table.insert_one(user_db)
    created_user = await table.find_one({'_id': new_user.inserted_id})
    
    return created_user

@app.get('/', response_model=List[UserRead])
async def list_users():
    users = await table.find().to_list(1000)

    return users

@app.get('/{id}', response_model=UserRead)
async def get_user(id: str):
    user = await table.find_one({'_id': id})

    if not user: raise HTTPException(status_code=404, detail=f'User not found')

    return user

@app.post('/{id}', response_model=UserRead)
async def update_user(id: str, user_update: UserUpdate):
    user_db = await table.find_one({'_id': id})

    if not user_db: raise HTTPException(status_code=404, detail=f'User not found')

    user_update = user_update.dict(exclude_unset=True)

    if len(user_update) >= 1:
        update_result = await table.update_one({"_id": id}, {"$set": user_update})

        if update_result.modified_count == 1:
            user_db = await table.find_one({'_id': id})

    return user_db
