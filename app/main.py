from fastapi import FastAPI,Depends, HTTPException, status  #depends is used to give the extra info for metadata by use of annotated
from pydantic import BaseModel
from app import database  #database package ah ithula import pannurom 
from typing import Annotated, List #it gives the hint to a metadata (extra info)
from sqlalchemy.orm import Session
from app import dbcon
from app import app_setting
from app import todoapi  
from app import hashpass
from app.routers import login
from app import access
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

origins=["*"]

app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"]
)

app.include_router(router=login.router, tags=["login"], prefix="/login")

@app.get('/userget')
async def user_get(db:Annotated[Session, Depends(database.get_db)]):
     user_retrive=db.query(dbcon.users).all()
     return user_retrive

@app.post('/userpost')
async def add_user(db:Annotated[Session, Depends(database.get_db)], users:todoapi.Usercreate):
     #print("PASSWORD LENGTH:", len(users.password))
     new_user=dbcon.users()
     new_user.password=hashpass.hash(users.password)
     new_user.username=users.username


     db.add(new_user)
     db.commit()
     db.refresh(new_user)

     return {"message":"Your Information added successfully"}

@app.get('/todos')                                                  #instead of username(decode) put token(encode) 
async def get_data(db:Annotated[Session, Depends(database.get_db)], username:Annotated[str,Depends(access.get_cur_username)]): 
    list_of_todo: List[dbcon.Todos]=db.query(dbcon.Todos).filter(dbcon.Todos.owner_username==username).all()     #instead of using get_cur_username put auth_scheme(if you use token(encode))
    return list_of_todo

@app.post('/todopost', status_code=status.HTTP_201_CREATED)                           #below username line use for auth the access token in decode form this help in validation part of user 
async def post_data(db:Annotated[Session, Depends(database.get_db)], Todo:todoapi.Todo, username:Annotated[str,Depends(access.get_cur_username)]):
     new_todo = dbcon.Todos(**Todo.dict(), owner_username=username)
     try:                                  #auth by acces_token in decode form it check the acess token are by which login useraname and only allow that user auther tables or columns
          db.add(new_todo)
          db.commit()
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="could not addd new todos")
     return{"result":"todos is created"}

@app.delete('/todo/{id}')
async def del_data(db:Annotated[Session, Depends(database.get_db)], id:int, username:Annotated[str,Depends(access.get_cur_username)]):
     id_query=db.query(dbcon.Todos).filter(dbcon.Todos.id==id, dbcon.Todos.owner_username==username)
     todo_id=id_query.first()  #first means deleted first matching rows ypu put second or all (all means delete all rows where id has in the table)

     if todo_id==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="ID was not exist")
     id_query.delete()
     db.commit()

     return{"result":"id is deleted successfully"}

@app.put('/todoup/{id}')
async def up_data(db:Annotated[Session,Depends(database.get_db)], id:int,Todo:todoapi.Todo, username:Annotated[str,Depends(access.get_cur_username)]):
     id_query=db.query(dbcon.Todos).filter(dbcon.Todos.id==id, dbcon.Todos.owner_username==username)
     todo_id=id_query.first()

     if todo_id==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Id is not exist")
     id_query.update(Todo.dict())
     db.commit()

     return {"result":"updated successfully"}


"""
#create the instance          localhost/docs , localhost/redoc =>see the output in different interface   
@app.get('/rt')
async def get_root():
     return {"response":"success"}

@app.get('/{id}')
async def get_path_op(id: int):
     return {"response" : f"path of variable is {id}"}


@app.get('/')
async def get_lim(query: str=None, limit: int=None):
     if query is not None and limit is not None:
          return{"query": f"query is {query}, limit is {limit}"}
     else:
          return{"response":"hello world"}


class students(BaseModel):
  name:str
  id: int
  About: str | None=None
  dept_id:int


@app.post('/details')
async def post_detail(item:students):
   return item


@app.get('/fetch')
async def get_data(db:Annotated[Session, Depends(database.get_db)]):  #db is just the variable name you use whatever you want
    all_result=db.query(dbcon.Tab).all()
    return all_result

@app.get('/todos')
async def get_data(db:Annotated[Session, Depends(database.get_db)]):  #db is just the variable name you use whatever you want
    list_of_todo: List[dbcon.Todos]=db.query(dbcon.Todos).all()
    return list_of_todo

@app.post('/todopost', status_code=status.HTTP_201_CREATED)
async def post_data(db:Annotated[Session, Depends(database.get_db)], Todo:todoapi.Todo):
     new_todo = dbcon.Todos(**Todo.dict())

     #  new_todo=dbcon.Todos()
     #  new_todo.title=Todo.title    we do like this also insteand of above line  new_todo=dbcon.Todos(**todo.model_dump())
     #  new_todo.list=Todo.list
    
     try:
          db.add(new_todo)
          db.commit()
     except Exception as e:
          raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="could not addd new todos")
     return{"result":"todos is created"}

@app.delete('/todo/{id}')
async def del_data(db:Annotated[Session, Depends(database.get_db)], id:int):
     id_query=db.query(dbcon.Todos).filter(dbcon.Todos.id==id)
     todo_id=id_query.first()  #first means deleted first matching rows ypu put second or all (all means delete all rows where id has in the table)

     if todo_id==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="ID was not exist")
     id_query.delete()
     db.commit()

     return{"result":"id is deleted successfully"}

@app.put('/todoup/{id}')
async def up_data(db:Annotated[Session,Depends(database.get_db)], id:int,Todo:todoapi.Todo):
     id_query=db.query(dbcon.Todos).filter(dbcon.Todos.id==id)
     todo_id=id_query.first()

     if todo_id==None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Id is not exist")
     id_query.update(Todo.dict())
     db.commit()

     return {"result":"updated successfully"}

"""

     