from app.app_setting import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic_settings import BaseSettings,SettingsConfigDict
from app import dbcon


settings=get_settings()

user=settings.user
password=settings.password
dsn=settings.dsn

engine=create_engine(f"oracle+oracledb://{user}:{password}@{dsn}")

#dbcon.Base.metadata.create_all(bind=engine)

def get_db():
    db=Session(engine)
    try:
        yield db
    finally:
        db.close()

