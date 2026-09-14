from fastapi import FastAPI

from routers import songs, users, items


app = FastAPI()
app.include_router(songs.router)
app.include_router(users.router)
app.include_router(items.router)
