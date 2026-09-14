from collections.abc import Sequence

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.song import Song
from schemas.song import SongCreate


async def list_songs(session: AsyncSession) -> Sequence[Song]:
    return (await session.exec(select(Song))).all()


async def create_song(session: AsyncSession, data: SongCreate) -> Song:
    song = Song(name=data.name, artist=data.artist)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
