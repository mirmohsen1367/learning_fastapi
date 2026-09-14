from pwdlib import PasswordHash
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate

password_hash = PasswordHash.recommended()


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
