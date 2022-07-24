import os
from fastapi import Depends, FastAPI

from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from app.controllers import hooks
from app.models import User
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    hooks.router,
    prefix="/hook",
    tags=["hooks"],
)

# add planet web project urls to CORS settings
PLANET_WEB_URL = os.environ.get("CLIENT_URL", "*")
# leave this to be able to set up "PLANET_WEB_URL=http://localhost:3000,http://localhost:80"
origins = PLANET_WEB_URL.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    pass

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
