import hashlib
import os
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    password_hash = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1
    )
    return f"scrypt${salt.hex()}${password_hash.hex()}"


@router.get("", response_model=list[UserPublic])
async def get_users(session: SessionDep):
    return (await session.exec(select(User))).all()


@router.post("", response_model=UserPublic, status_code=201)
async def add_user(user: UserCreate, session: SessionDep):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
