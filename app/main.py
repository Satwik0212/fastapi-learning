from fastapi import FastAPI,Body, Response, status, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg.rows import dict_row

app = FastAPI() #creates a FastAPI Application Object.

class Post(BaseModel) :
    title: str 
    content: str 
    published: bool = True # if no value is given in the JSON it automatically makes it true.
    rating: Optional[int] = None # means it can be an integer or None.

try:
    conn = psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='Akki_2026.', row_factory=dict_row)
    print("connection successfull")
except psycopg.OperationalError as e:
    print(f"connection failed: {e}")

#my_posts = [{"title" : "title post 1", "content" : "content of post 1","id": 1}, {"title" : "favourite foods", "content": "I like apples", "id" : 2}]
#The slash means Homepages , it is called a root path.

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"message": "Hello World"} #JSON data is returned (key:value)
    
@app.get("/posts")
async def get_posts():
    post = conn.execute("SELECT * FROM posts;").fetchall()

    return {"data": post}
    

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    new_posts = conn.execute("""INSERT INTO posts ("title", "content", "published") VALUES (%s,%s,%s) RETURNING *; """, 
                            (post.title, post.content, post.published)).fetchone()
    conn.commit()
    return {"data" : new_posts}

#@app.get("/posts/{id}")
#def get_post(id: int):
 #   print(id)
  #  for post in my_posts:
  #      if post["id"] == id:
   #         return post
   # return {"post_detail": f"Here is post {id}"}

                   #OR

@app.get("/posts/{id}")
def get_post(id: int, response:Response):
    post = conn.execute(f"SELECT * FROM posts WHERE id = {id}" ).fetchone()
    if not post:
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id: {id} was not found"}
                           #OR

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    return {"post details" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
    deleted_post = conn.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (id,)).fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, response: Response):
    updated_post = conn.execute("UPDATE posts SET title = %s WHERE id = %s RETURNING *;", ("updated title", id)).fetchone()
    conn.commit()
    if not updated_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    return {"message" : "post was successfully updated", "data": updated_post}