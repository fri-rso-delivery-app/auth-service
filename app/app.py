from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.config import Settings, get_settings

settings: Settings = get_settings()

app = FastAPI(
    root_path=settings.api_root_path,
    title='Authentication microservice',
)

allowed_origins = ([
        'http://localhost:8888',
        'http://0.0.0.0:8888',
    ]
    # allow localhost ports from 8000-8009
    + [f'http://localhost:{8000+i}' for i in range(10)]
    + [f'http://0.0.0.0:{8000+i}' for i in range(10)]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# auth router
from app.routers import jwt
app.include_router(jwt.router)

# user profiles router
from app.routers import users
app.include_router(users.router)


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return f"""
        <h1> Hello! Docs available at <a href="{request.scope.get("root_path")}/docs">{request.scope.get("root_path")}/docs</a> </h1>
    """

