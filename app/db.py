import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
for scheme in ("postgres://", "postgresql://", "postgresql+psycopg2://"):
    if DATABASE_URL.startswith(scheme):
        DATABASE_URL = DATABASE_URL.replace(scheme, "postgresql+asyncpg://", 1)
        break

engine = create_async_engine(DATABASE_URL, echo=True)
session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session
