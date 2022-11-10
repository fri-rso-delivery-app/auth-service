from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


app = FastAPI(
    title='Authentication microservice',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# auth router
#from app.routers.auth import auth
#app.include_router(auth.router)

# user profiles router
from app.routers import users
app.include_router(users.router)


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return f"""
        <h1> Hello! Docs available at <a href="{request.scope.get("root_path")}/docs">{request.scope.get("root_path")}/docs</a> </h1>
    """

