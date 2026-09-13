from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import engine, get_session
from app.models import Song, SongCreate, SongPublic


app = FastAPI()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[SongPublic])
async def get_songs(session: AsyncSession = Depends(get_session)):
    return (await session.exec(select(Song))).all()


@app.post("/songs", response_model=SongPublic, status_code=201)
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
