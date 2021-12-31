from fastapi import FastAPI, Depends, status, Response, HTTPException
from typing import List
from . import schemas, models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .hashing import Hash
from .routers import blog, user

app = FastAPI()

# this line checks all the models and creates the tables
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
