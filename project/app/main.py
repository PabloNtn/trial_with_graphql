from fastapi import FastAPI
from .schema import graphql_app
from .models import init_db

app = FastAPI()
@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(graphql_app, prefix='/graphql')