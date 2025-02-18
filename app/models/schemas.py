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

class CinemaSchema(CinemaBase):
    id: int

    class Config:
        orm_mode = True


# Base para criação e atualização
class FilmeBase(BaseModel):
    titulo: str
    sinopse: str
    duracao: int
    diretor_id: int

    class Config:
        orm_mode = True  # Permite conversão automática entre SQLAlchemy e Pydantic


# Para criar um novo filme
class FilmeCreate(FilmeBase):
    pass


# Para resposta (inclui ID)
class FilmeSchema(FilmeBase):
    id: int  # O ID será retornado nas respostas
