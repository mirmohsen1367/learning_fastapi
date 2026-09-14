import math

from pwdlib import PasswordHash
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.user import User
from schemas.user import UserCreate, UserPage

password_hash = PasswordHash.recommended()


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
