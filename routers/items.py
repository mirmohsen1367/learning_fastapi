from typing import Annotated
from fastapi import APIRouter, Depends, BackgroundTasks

router = APIRouter(prefix="/items", tags=["items"])


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_task: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_task.add_task(write_log, message)
    return q


@router.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}