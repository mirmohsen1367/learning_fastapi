from sqlmodel import Field, SQLModel


class Song(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    artist: str
    test: str | None = None

class Album(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    year: int | None = None
    test: str | None = None
