from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Substitua pelo seu banco de dados, no caso SQLite assíncrono
DATABASE_URL = "sqlite+aiosqlite:///./cineAPI.db"

# Criando o engine assíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Criando uma session maker assíncrona
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Base de modelos
Base = declarative_base()

# Função para obter a sessão do banco de dados
async def init_db():
    async with engine.begin() as conn:
        # Cria todas as tabelas no banco de dados
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with SessionLocal() as session:
        yield session