import random
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel  # Data validation and settings management
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from starlette.routing import Host  # import column of the table

app=FastAPI()
#order impact top to bottom approach
#uvicorn myapi:app --reload
class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating: Optional[int] = None

try:
    conn = psycopg2.connect(host='localhost',database='postgres',user='postgres', password= 'askme123', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connecting to database sucessfully!")

except Exception as error:
    print("connecting database failed")
    print(f"Error : {error}")
#my_posts = [{"title":"The Book u never forget", "content":"All the world","author":"Harry", "id":1},
#{"title":"Forgot the Memory", "content":"Nothing is imposibble", "author":"John", "id":2}]

@app.get("/")
async def root():
    return {"message": "Welcome to my world"}

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p

@app.get("/posts")
def get_post():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

#----------------------------------------------------
# status code from status
# Exception from HTTPException 
#----------------------------------------------------

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s,%s,%s) RETURNING *""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000)
    # my_posts.append(post_dict)
    #print(post.dict())  # Converts any pydentic model to a dictionary
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int,response: Response):
    #print(id)
    #post=find_post(id)
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
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
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} was not present.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id={id} was not present."}
    # index = find_post(id)
    # my_posts.pop(index)
    return {"message": "Post has been deleted."}

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with id={id} was not present.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id={id} was not present."}
    return {"data": updated_post}