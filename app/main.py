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

models.Base.metadata.create_all(bind=engine)

app = FastAPI() #creates a FastAPI Application Object.
#..

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

@app.get("/")
async def root():
    return {"message": "Hello World"} #JSON data is returned (key:value)
    
@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post
    

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
    
    
    #new_posts = conn.execute("""INSERT INTO posts ("title", "content", "published") VALUES (%s,%s,%s) RETURNING *; """, 
     #                       (post.title, post.content, post.published)).fetchone()
    #conn.commit()
    #return {"data" : new_posts}

#@app.get("/posts/{id}")
#def get_post(id: int):
 #   print(id)
  #  for post in my_posts:
  #      if post["id"] == id:
   #         return post
   # return {"post_detail": f"Here is post {id}"}

                   #OR

@app.get("/posts/{id}")
def get_post(id: int, response:Response,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id: {id} was not found"}
                           #OR

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    return post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):
    # 1. Create a query for the post
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # 2. Check if the post exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id : {id} was not found"
        )
    
    # 3. Perform the update using the schema payload dictionary
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    
    # 4. Commit changes to the database
    db.commit()

    # 5. Return the updated post
    return post_query.first()

                                #USERS

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
   
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(email = user.email, password = user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{id}", response_model = schemas.UserOut)
async def get_user(id: int, response:Response,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"User with id : {id} was not found")
    return user