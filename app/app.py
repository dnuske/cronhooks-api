import os
from time import sleep
import logging
from multiprocessing import Process
import signal

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, current_active_user, fastapi_users
from app.controllers import hooks
from app.models import User

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



class GracefulExit(Exception):
    pass


def signal_handler(signum, frame):
    raise GracefulExit()

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())


def f(name):
    info('function f')
    print('hello', name)

    try:
        while (True):
            print("yeah")

            sleep(5)
    except GracefulExit:
        print("Subprocess exiting gracefully")
    print(" ===== finish starting up ====== ")




@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    print(" ===== STARTING UP HOOKS PROCESS ====== ")
    # TODO: catch SIGTERM and pass it on to the subprocess
    signal.signal(signal.SIGTERM, signal_handler)

    p = Process(target=f, args=('bob',))
    p.start()

@app.on_event("shutdown")
def shutdown_event():
    print(" ===== shutting down ====== ")

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
