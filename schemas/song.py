from sqlmodel import SQLModel


class SongCreate(SQLModel):
    name: str
    artist: str


class SongPublic(SongCreate):
    id: int
