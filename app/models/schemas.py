from pydantic import BaseModel

class CinemaBase(BaseModel):
    nome: str
    endereco: str
    cidade: str
    estado: str
    capacidade: int | None = None

    class Config:
        orm_mode = True  # Isso permite que o Pydantic entenda os modelos do SQLAlchemy

class CinemaCreate(CinemaBase):
    pass

class Cinema(CinemaBase):
    id: int

    class Config:
        orm_mode = True