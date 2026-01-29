from datetime import datetime, timedelta
from jose import jwt, JWTError #JSON Web Token 
from app.app_setting import get_settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI,Depends, HTTPException, status  #depends is used to give the extra info for metadata by use of annotated
from app import database  #database package ah ithula import pannurom 
from typing import Annotated, List 

auth_scheme=OAuth2PasswordBearer(tokenUrl='/login')

settings=get_settings()

def cre_access_token(data:dict):
    data_copy=data.copy()
    expiration_time=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_MINUTES)
    data_copy.update({"exp": expiration_time})
    token=jwt.encode(data_copy, algorithm=settings.ALGORITHM, key=settings.SECRET_KEY)
    return token


#it is not working 
def get_cur_username(token:Annotated[str, Depends(auth_scheme)]):
    
    try:
        payload=jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str =payload.get('username')

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials")
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate Credentials")

    return username