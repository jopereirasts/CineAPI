from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Date, Time
from sqlalchemy.orm import relationship
from config.database import Base
from enum import Enum as PyEnum
import datetime

class TipoUsuario(PyEnum):
    diretor = "diretor"
    espectador = "espectador"

class PapelTrabalhador(PyEnum):
    diretor = "diretor"
    ator = "ator"
    roteirista = "roteirista"
    tecnico = "tecnico"

class Cinema(Base):
    __tablename__ = "cinemas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    endereco = Column(String)
    cidade = Column(String)
    estado = Column(String)
    capacidade = Column(Integer, nullable=True)

class Filme(Base):
    __tablename__ = "filmes"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    sinopse = Column(String)
    duracao = Column(Integer)
    diretor_id = Column(Integer, ForeignKey("diretores.id"))
    diretor = relationship("Diretor", back_populates="filmes")

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)
    senha = Column(String)
    tipo_usuario = Column(Enum(TipoUsuario))

class Diretor(Base):
    __tablename__ = "diretores"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    biografia = Column(String)
    usuario = relationship("Usuario")
    filmes = relationship("Filme", back_populates="diretor")

class Espectador(Base):
    __tablename__ = "espectadores"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario")

class Exibicao(Base):
    __tablename__ = "exibicoes"
    
    id = Column(Integer, primary_key=True, index=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"))
    cinema_id = Column(Integer, ForeignKey("cinemas.id"))
    data_exibicao = Column(Date)
    horario_exibicao = Column(Time)
    filme = relationship("Filme")
    cinema = relationship("Cinema")

class TrabalhadorFilme(Base):
    __tablename__ = "trabalhadores_filme"
    
    id = Column(Integer, primary_key=True, index=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"))
    nome = Column(String)
    papel = Column(Enum(PapelTrabalhador))
    filme = relationship("Filme")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"))
    espectador_id = Column(Integer, ForeignKey("espectadores.id"))
    nota = Column(Integer, nullable=False)
    comentario = Column(String, nullable=True)
    data_avaliacao = Column(DateTime, default=datetime.datetime.utcnow)  
    filme = relationship("Filme")
    espectador = relationship("Espectador")