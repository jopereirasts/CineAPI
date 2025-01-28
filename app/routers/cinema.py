from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter()

@router.post("/")
async def create_cinema(cinema: "Cinema", db: Session = Depends(get_db)):  # Usando string para evitar o ciclo de importação
    from app.models import Cinema  # Importação local para evitar o ciclo
    db.add(cinema)
    await db.commit()  # Commit assíncrono
    await db.refresh(cinema)  # Atualiza o objeto após commit
    return cinema

@router.get("/cinemas")
async def get_cinemas():
    return {"cinemas": "Lista de cinemas aqui"}

@router.get("/")
async def get_cinemas(db: Session = Depends(get_db)):
    from app.models import Cinema  # Importação local para evitar o ciclo
    async with db.begin():  # Usando transação assíncrona
        result = await db.execute(select(Cinema))
        cinemas = result.scalars().all()
    return cinemas

@router.get("/{cinema_id}")
async def get_cinema(cinema_id: int, db: Session = Depends(get_db)):
    from app.models import Cinema  # Importação local para evitar o ciclo
    result = await db.execute(select(Cinema).filter(Cinema.id == cinema_id))
    cinema = result.scalar_one_or_none()
    if cinema is None:
        raise HTTPException(status_code=404, detail="Cinema não encontrado")
    return cinema