from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Identity,Integer,String,Column,ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import func

class Base(DeclarativeBase):
    pass


class Todos(Base):
    __tablename__="todos"
    id_identity=Identity(start=1, increment=1)
    id=Column(Integer, id_identity, primary_key=True)
    title=Column(String(50), unique=True, nullable=False)
    description=Column(String(100), nullable=False)
    owner_username=Column(String(100), ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp())

class users(Base):
    __tablename__="users"
    id_identity=Identity(start=1, increment=1)
    id=Column(Integer, id_identity, primary_key=True)   
    username=Column(String(50), unique=True, nullable=False)
    password=Column(String(100), nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.current_timestamp())

"""
class Tab(Base):
    __tablename__="register_stu"
    id_identity=Identity(start=1, increment=1)
    id=Column(Integer, id_identity, primary_key=True)

    name=Column(String(50), unique=True, nullable=False)
"""