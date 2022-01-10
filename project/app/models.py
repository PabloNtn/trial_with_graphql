import os
from sqlmodel import (
    SQLModel,
    Field,
    create_engine,
    default,
    select,
    Session,
    Relationship
)
from typing import Optional,List

dataBase_Url = os.environ.get("DATABASE_URL")

engine = create_engine(dataBase_Url, echo=True, future=True)

class Pessoa(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    nome :str
    idade:int

    books: List['Book'] = Relationship(back_populates='pessoa')

class Book(SQLModel, table=True):
    id:Optional[int] = Field(default=None, primary_key=True)
    titulo :str
    
    pessoa_id: Optional[int] = Field(default=None, foreign_key="pessoa.id")
    pessoa: Optional[Pessoa] = Relationship(back_populates='books')

async def init_db():
   SQLModel.metadata.create_all(engine)

