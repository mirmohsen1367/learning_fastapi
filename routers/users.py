from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from schemas.user import UserCreate, UserPublic
from services import users as user_service

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.post("", response_model=UserPublic, status_code=201)
async def add_user(user: UserCreate, session: SessionDep):
    return await user_service.create_user(session, user)
