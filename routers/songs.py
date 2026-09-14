from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from db import get_session
from schemas.song import SongCreate, SongPublic
from services import songs as song_service

router = APIRouter(prefix="/songs", tags=["songs"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[SongPublic])
async def get_songs(session: SessionDep):
    return await song_service.list_songs(session)


@router.post("", response_model=SongPublic, status_code=201)
async def add_song(song: SongCreate, session: SessionDep):
    return await song_service.create_song(session, song)
