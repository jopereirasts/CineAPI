from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.models import Cinema
from config.database import get_db

router = APIRouter()

class CinemaCreate(BaseModel):
    nome: str
    endereco: str
    cidade: str
    estado: str
    capacidade: int

@router.post("/cinemas")
async def create_cinema(cinema: CinemaCreate, db: AsyncSession = Depends(get_db)):
    novo_cinema = Cinema(**cinema.dict())  # Criando o objeto
    db.add(novo_cinema)
    await db.flush()  # Flush para garantir que a transação seja escrita
    await db.commit()  # Commit para persistir no banco
    await db.refresh(novo_cinema)  # Atualiza o objeto para refletir os dados persistidos
    return novo_cinema

# Função para pegar os cinemas
@router.get("/cinemas")
async def get_cinemas(db: AsyncSession = Depends(get_db)):  # Usando AsyncSession
    result = await db.execute(select(Cinema))
    cinemas = result.scalars().all()
    return cinemas

# Função para pegar cinema específico
@router.get("/cinemas/{cinema_id}")
async def get_cinema(cinema_id: int, db: AsyncSession = Depends(get_db)):  # Usando AsyncSession
    result = await db.execute(select(Cinema).filter(Cinema.id == cinema_id))
    cinema = result.scalar_one_or_none()  # Mudando de `scalar()` para `scalar_one_or_none()`
    if cinema is None:
        raise HTTPException(status_code=404, detail="Cinema não encontrado")
    return cinema