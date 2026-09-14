from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import SQLModel


EMAIL_PATTERN = r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
Email = Annotated[
    str, StringConstraints(pattern=EMAIL_PATTERN, max_length=320)
]
Username = Annotated[str, StringConstraints(min_length=3, max_length=50)]
Password = Annotated[str, StringConstraints(min_length=8, max_length=128)]


class UserCreate(SQLModel):
    username: Username
    email: Email
    password: Password


class UserPublic(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool


class UserPage(SQLModel):
    items: list[UserPublic]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    next_page: int | None
    previous_page: int | None


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
