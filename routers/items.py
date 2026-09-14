from typing import Annotated
from fastapi import APIRouter, Depends


# arouter = APIRouter(prefix="/items", tags=["items"])

# def create_test(username: str, password: str):
#     return {"username": username, "password": password}

# class Authservice:
#     def __init__(self, secret=None, secret_1=None):
#         self.secret = secret
#         self.secret_1 = secret_1

# @router.get("/test_id/{test_id}")
# async def test(test_id: int, test: Authservice =Depends(Authservice)):
#     return test.secret_1
# async def test(test=Depends(create_test)):
#     return {"test": test}

# ----------------------------------------------------------------------------------
# add nested dependencies

router = APIRouter(prefix="/items", tags=["items"])

# Runs first because second_dependency needs its result.
def first_dependency(test):
    print("1. first_dependency runs")
    return "Hello"


# # FastAPI passes the first dependency's return value into message.
# def second_dependency(message: Annotated[str, Depends(first_dependency)]):
#     print("2. second_dependency runs")
#     return message + " from items"


# @router.get("/{test_id}")
# def read_items(test_id: Annotated[str, Depends(first_dependency)]):
#     print("3. read_items runs")
#     return {"message": test_id}


def first_dependency(ss: str):
    return f"processed-{ss}"


@router.get("/{test_id}")
def read_items(
    test_id: str,
    result: Annotated[str, Depends(first_dependency)],
):
    return {
        "test_id": test_id,
        "result": result,
    }