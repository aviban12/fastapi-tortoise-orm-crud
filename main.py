# pylint: disable=E0611,E0401
from sqlite3 import Date
from typing import List
from datetime import datetime
from xmlrpc.client import DateTime
import bcrypt
from fastapi import FastAPI, HTTPException
from models import User_Pydantic, UserIn_Pydantic, Users
from pydantic import BaseModel
import uvicorn
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from datetime import date
app = FastAPI()

class userModel(BaseModel):
    first_name: str
    last_name: str
    join_date: date
    password: str


class Status(BaseModel):
    message: str


@app.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@app.post("/users", response_model=User_Pydantic)
async def create_user(user: userModel):
    user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    user_obj = await Users.create(**user.dict(exclude_unset=False))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get(
    "/user/{user_id}", responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@app.put(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: userModel):
    user.password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@app.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")

register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)