from app.app_setting import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pydantic_settings import BaseSettings,SettingsConfigDict
from app import dbcon


settings=get_settings()

user=settings.user
password=settings.password
dsn=settings.dsn

DATABASE_URL=f"oracle+oracledb://{user}:{password}@{dsn}"
engine = create_engine(
    DATABASE_URL, 
    connect_args={
        "expire_time": 2, 
        "tcp_connect_timeout": 20
    }
)

#dbcon.Base.metadata.create_all(bind=engine)

def get_db():
    db=Session(engine)
    try:
        yield db
    finally:
        db.close()

