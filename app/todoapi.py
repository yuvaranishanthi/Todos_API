from pydantic import BaseModel,Field

class Todo(BaseModel):
    title: str
    description: str

class Usercreate(BaseModel):
    username: str
    password: str=Field(min_length=6, max_length=72)

    

#git init
#git add .
#git commit -m "Initial project commit"
#git push -u origin main
#git remote add origin https://github.com/yuvashanthiTodos_API.git
#git branch -M main       
#git push -u origin main
