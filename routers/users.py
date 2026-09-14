from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from schemas.user import Token, UserCreate, UserPage, UserPublic
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


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user = await user_service.authenticate_user(
        session, form_data.username, form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=user_service.create_access_token(user.username),
        token_type="bearer",
    )
