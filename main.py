from fastapi import FastAPI

from routers import songs
from routers import users


app = FastAPI()
app.include_router(songs.router)
app.include_router(users.router)
