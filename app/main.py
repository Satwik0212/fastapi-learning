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

my_posts = [{"title" : "title post 1", "content" : "content of post 1","id": 1}, {"title" : "favourite foods", "content": "I like apples", "id" : 2}]
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
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

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
    post = find_post(id)
    if not post:
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id: {id} was not found"}
                           #OR

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    return {"post details" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    my_posts.pop(index)
    return {"message" : "post was successfully deleted"}

@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, response: Response):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    post = my_posts[index]
    post["title"] = "updated title"
    return {"message" : "post was successfully updated"}