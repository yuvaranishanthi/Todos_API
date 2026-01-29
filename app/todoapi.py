from pydantic import BaseModel,Field

class Todo(BaseModel):
    title: str
    description: str

class Usercreate(BaseModel):
    username: str
    password: str=Field(min_length=6, max_length=72)


#git commit -m "Initial project commit"


#git branch -M main
#git push -u origin main
