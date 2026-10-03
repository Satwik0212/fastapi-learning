from fastapi import FastAPI,Body, Response, status, HTTPException, Depends
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, users, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI() #creates a FastAPI Application Object.
#..

#In main.py we are including the routers of the other modules.
#The path will be /posts and /users

app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
#try:
 #   conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Akki_2026.', row_factory=dict_row)
  #  print("connection successfull")
#except psycopg.OperationalError as e:
 #   print(f"connection failed: {e}")

#my_posts = [{"title" : "title post 1", "content" : "content of post 1","id": 1}, {"title" : "favourite foods", "content": "I like apples", "id" : 2}]
#The slash means Homepages , it is called a root path.

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
# 
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i

                                #USERS

