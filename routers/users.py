from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from schemas.user import UserCreate, UserPage, UserPublic
from services import users as user_service

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=UserPage)
async def get_users(
    session: SessionDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return await user_service.list_users(session, page, page_size)


@router.post("", response_model=UserPublic, status_code=201)
async def add_user(user: UserCreate, session: SessionDep):
    return await user_service.create_user(session, user)
