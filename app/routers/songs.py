from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.models.song import Song
from app.schemas.song import SongCreate, SongPublic

router = APIRouter(prefix="/songs", tags=["songs"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[SongPublic])
async def get_songs(session: SessionDep):
    return (await session.exec(select(Song))).all()


@router.post("", response_model=SongPublic, status_code=201)
async def add_song(song: SongCreate, session: SessionDep):
    db_song = Song(name=song.name, artist=song.artist)
    session.add(db_song)
    await session.commit()
    await session.refresh(db_song)
    return db_song
