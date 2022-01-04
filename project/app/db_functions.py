from sqlalchemy.orm import joinedload
from sqlmodel import Session, select
from .models import Pessoa, engine, Book

def create_pessoas(idade: int, nome: str):
    person = Pessoa(nome = nome, idade = idade)    
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
    return person

def create_books(titulo: str, pessoa_id:int):
    book = Book(titulo=titulo, pessoa_id=pessoa_id)    
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
    return book

def get_pessoas(idade:int = None, limit:int = None):
    query = select(Pessoa)
    if idade:
        query = query.where(Pessoa.idade == idade)
    if limit:
        query= query.limit(limit)
    with Session(engine) as session:
        result = session.execute(query).scalars().all()
        
    return result

def get_books():
    query = select(Book).options(joinedload('*'))
    
    with Session(engine) as session:
        result = session.execute(query).scalars().unique().all()    
    return result