import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel  # Data validation and settings management
from random import randrange 
app=FastAPI()
#order impact top to bottom approach
#uvicorn myapi:app --reload
class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title":"The Book u never forget", "content":"All the world","author":"Harry", "id":1},
{"title":"Forgot the Memory", "content":"Nothing is imposibble", "author":"John", "id":2}]

@app.get("/")
async def root():
    return {"message": "Welcome to my world"}

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get("/posts")
def get_post():
    return {"data": my_posts}

#----------------------------------------------------
# status code from status
# Exception from HTTPException 
#----------------------------------------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,1000000)
    my_posts.append(post_dict)
    #print(post.dict())  # Converts any pydentic model to a dictionary
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    #print(id)
    post=find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} was not present.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id={id} was not present."}
    return {"data": post}

#-----------------------------------------
#Order matters in API creation
#top down approach in route selection
#-----------------------------------------

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = find_post(id)
    my_posts.pop(index)
    return {"message": "Post has been deleted."}


