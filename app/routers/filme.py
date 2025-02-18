from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.models import Filme
from config.database import get_db
from app.models.schemas import FilmeSchema, FilmeCreate

router = APIRouter()

class FilmeCreate(BaseModel):
    titulo: str
    sinopse: str
    duracao: int
    diretor_id: int

@router.post("/filmes", response_model=FilmeSchema)
async def create_filme(filme: FilmeCreate, db: AsyncSession = Depends(get_db)):
    novo_filme = Filme(**filme.dict())  
    db.add(novo_filme)
    await db.flush()  
    await db.commit()
    await db.refresh(novo_filme)
    return novo_filme

@router.get("/filmes")
async def get_filmes(db: AsyncSession = Depends(get_db)):  # Usando AsyncSession
    result = await db.execute(select(Filme))
    filmes = result.scalars().all()
    return filmes

@router.get("/filmes/{filme_id}")
async def get_filme(filme_id: int, db: AsyncSession = Depends(get_db)):  # Usando AsyncSession
    result = await db.execute(select(Filme).filter(Filme.id == filme_id))
    filme = result.scalar_one_or_none()  # Mudando de `scalar()` para `scalar_one_or_none()`
    if filme is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme

@router.put("/filmes/{filme_id}", response_model=FilmeSchema) 
async def update_filme(filme_id: int, filme: FilmeCreate, db: AsyncSession = Depends(get_db)):
    db_filme = await db.execute(select(Filme).filter(Filme.id == filme_id))
    db_filme = db_filme.scalar_one_or_none()
    
    if db_filme is None:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    
    db_filme.titulo = filme.titulo
    db_filme.sinopse = filme.sinopse
    db_filme.duracao = filme.duracao
    db_filme.diretor_id = filme.diretor_id

    await db.commit()
    await db.refresh(db_filme)
    
    return db_filme

@router.delete("/filmes/{filme_id}")
async def delete_filme(filme_id: int, db: AsyncSession = Depends(get_db)):
    # Verifica se o filme existe
    result = await db.execute(select(Filme).filter(Filme.id == filme_id))
    filme = result.scalar_one_or_none()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    # Deleta o filme
    await db.delete(filme)
    await db.commit()  # Commit assíncrono
    return {"detail": f"Filme com ID {filme_id} excluído com sucesso"}