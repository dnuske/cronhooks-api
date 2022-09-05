from fastapi import APIRouter, Depends
from app.db import db
from app.scheduler.schedule_manager import determine_next_schedule
from app.utils import JsonDatatype, HookDatatype
from app.users import fastapi_users, current_active_user
from app.models import User
from datetime import datetime

router = APIRouter(prefix="")

current_user = fastapi_users.current_user()

@router.get("/", tags=["hooks"])
async def get_hooks(user: User = Depends(current_active_user)):
    return await db.get_all_hooks(user.id)


@router.post("/", tags=["hooks"])
async def create_hook(hook: HookDatatype, user: User = Depends(current_active_user)):
    return await db.create_hook(hook, user.id)


@router.get("/{id}", tags=["hooks"])
async def get_hook(id: str, user: User = Depends(current_active_user)):
    if db.hook_belongs_to_user(id, user.id):
        return await db.get_hook(id)


@router.put("/{id}", tags=["hooks"])
async def update_hook(id: str, hook: HookDatatype, user: User = Depends(current_active_user)):
    hook.id = id
    if db.hook_belongs_to_user(id, user.id):
        return await db.update_hook(hook)


@router.delete("/{id}", tags=["hooks"])
async def delete_hook(id: str, user: User = Depends(current_active_user)):
    if db.hook_belongs_to_user(id, user.id):
        return await db.delete_hook(id)


@router.get("/{id}/hits", tags=["hooks"])
async def get_hook_hits(id: str, user: User = Depends(current_active_user)):
    if db.hook_belongs_to_user(id, user.id):
        return await db.get_all_hook_hits(id)

