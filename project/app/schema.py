from strawberry.fastapi import GraphQLRouter
from typing import Optional,List

from strawberry.scalars import ID
from .db_functions import (
                            create_pessoas, 
                            get_pessoas, 
                            get_books, 
                            create_books, 
                            delete_pessoa, 
                            update_pessoa
                            )
import strawberry

from graphql import  GraphQLObjectType


@strawberry.type
class Pessoa:
    id:Optional[int]
    nome:str
    idade:int
    books: List['Book']

@strawberry.type
class Book:
    id:Optional[int]
    titulo:str
    pessoa: Pessoa

@strawberry.type
class Query:
    all_pessoa: list[Pessoa] = strawberry.field(resolver=get_pessoas)
    all_book: list[Book] = strawberry.field(resolver=get_books)

@strawberry.type
class Mutation:
        create_pessoa: list[Pessoa] = strawberry.field(resolver=create_pessoas)
        create_book: Book = strawberry.field(resolver=create_books)
        delete_pessoa: str = strawberry.field(resolver=delete_pessoa)
        update_pessoa: list[Pessoa] = strawberry.field(resolver = update_pessoa)
            

schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(schema)