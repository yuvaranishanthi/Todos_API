from fastapi import APIRouter
from fastapi import FastAPI,Depends, HTTPException, status  #depends is used to give the extra info for metadata by use of annotated
from app import database  #database package ah ithula import pannurom 
from typing import Annotated, List #it gives the hint to a metadata (extra info)
from sqlalchemy.orm import Session
from app import dbcon
from app import app_setting
from app import todoapi
from app.hashpass import hash
from app import hashpass
from fastapi.security import OAuth2PasswordRequestForm  #Swagger UI shows a username/password login box here
from app import access

router=APIRouter()

@router.post('/')
async def login(db:Annotated[Session,Depends(database.get_db)], user_cre:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user=db.query(dbcon.users).filter(dbcon.users.username==user_cre.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if hashpass.verify(user_cre.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credential")
    
    #we implement to generating the access token
    access_token=access.cre_access_token({"username":user.username})
    return{"Access Token":access_token, "token_type":"bearer"}