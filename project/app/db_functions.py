import typing
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.schema import Identity
from sqlmodel import Session, select
from strawberry.scalars import ID
from .models import Pessoa, engine, Book
from typing import List
from sqlalchemy.sql import func, select, table, column
from typing import NewType

from strawberry.custom_scalar import scalar

name_list = scalar(NewType("name_list", str))

idade_list = scalar(NewType("idade_list", int))

def create_pessoas(name:typing.List[name_list],idade:typing.List[idade_list]):
    i=0
    obj = []
    person = []
    for nome in name:
        obj += [Pessoa(nome=name[i], idade = idade[i])]
        i = i+1 
    with Session(engine) as session:
        session.add_all(obj)
        session.commit()
    return person

def create_books(titulo: str, pessoa_id:int):
    book = Book(titulo=titulo, pessoa_id=pessoa_id)    
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
    return book
#idade:int = None,  limit:int = None
def get_pessoas():
    query = select(Pessoa)
    # if idade:
    #     query = query.where(Pessoa.idade == idade)
    # if limit:
    #     query= query.limit(limit)
    my_table = table('pessoa', column('idade'))
    with Session(engine) as session:
        
        #.execute(query).scalars().all()
        #select(func.count()).select_from(my_table)
        #session.query(func.sum(Pessoa.idade).label("mac"))
        qr = select(func.count()).select_from(Pessoa).where(Pessoa.idade == 19)
        # result = qr.one()
        # max = result.mac
        result = session.execute(qr).scalars().all()
        
    return result

def get_books():
    query = select(Book).options(joinedload('*'))
    
    with Session(engine) as session:
        result = session.execute(query).scalars().unique().all()    
    return result

def delete_pessoa(id:int):
    with Session(engine) as session:
        query = select(Pessoa)
        if id:
            query = query.where(Pessoa.id == id)
        result = session.exec(query)
        person = result.one()
        session.delete(person)
        session.commit()
        result = "Deletado com succeso"   
    return result

def update_pessoa(id:ID, nome:str, idade:int):
    with Session(engine) as session:
        query = select(Pessoa)
        if id:
            query = query.where(Pessoa.id == id)
        search = session.exec(query)
        person = search.one()

        person.nome = nome
        person.idade = idade
        session.add(person)
        session.commit()
        session.refresh(person)
    return person