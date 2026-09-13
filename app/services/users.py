import hashlib
import os
from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    password_hash = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1
    )
    return f"scrypt${salt.hex()}${password_hash.hex()}"


async def list_users(session: AsyncSession) -> Sequence[User]:
    return (await session.exec(select(User))).all()


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
