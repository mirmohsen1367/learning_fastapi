from fastapi import FastAPI

from app.routers import songs, users

app = FastAPI()
app.include_router(songs.router)
app.include_router(users.router)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
