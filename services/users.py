import math
import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User
from schemas.user import UserCreate, UserPage

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")
JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def list_users(
    session: AsyncSession, page: int, page_size: int
) -> UserPage:
    total = (await session.exec(select(func.count()).select_from(User))).one()
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    statement = select(User).order_by(User.id).offset(offset).limit(page_size)
    users = (await session.exec(statement)).all()

    return UserPage(
        items=users,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_previous=page > 1,
        next_page=page + 1 if page < total_pages else None,
        previous_page=page - 1 if page > 1 else None,
    )


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=password_hash.hash(data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> User | None:
    user = (
        await session.exec(select(User).where(User.username == username))
    ).first()
    if user is None:
        password_hash.verify(password, DUMMY_HASH)
        return None
    if not password_hash.verify(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user


def create_access_token(username: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"sub": username, "exp": expires_at},
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )
