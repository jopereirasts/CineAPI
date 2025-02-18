from fastapi import FastAPI
from config.database import init_db
from app.routers import cinema
from app.routers import filme

app = FastAPI()

app.include_router(cinema.router)
app.include_router(filme.router)

@app.on_event("startup")
async def on_startup():
    # Cria as tabelas no banco de dados se ainda não existirem
    await init_db()

@app.get("/")
async def root():
    return {"message": "Bem-vindo à CineAPI, um espaço de Cinema Independente!"}