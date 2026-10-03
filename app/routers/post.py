from .. import models, schemas, utils
from .. database import engine, SessionLocal, get_db
from fastapi import FastAPI,Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
 ) #this is used for modularity of the code , so that we can have routers of all the components in the project , instead of having it in single main.py file.

@router.get("/")
async def root():
    return {"message": "Hello World"} #JSON data is returned (key:value)
    
@router.get("/")
async def get_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    return post
    

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
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

@router.get("/{id}")
def get_post(id: int, response:Response,  db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        #response.status_code= status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id: {id} was not found"}
                           #OR

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, response: Response, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , 
                            detail = f"Post with id : {id} was not found")
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK)
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

