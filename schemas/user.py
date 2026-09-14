from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import SQLModel


EMAIL_PATTERN = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
Email = Annotated[str, StringConstraints(pattern=EMAIL_PATTERN)]


class UserCreate(SQLModel):
    username: str
    email: Email
    password: str


class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str | None = None


class User(SQLModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
