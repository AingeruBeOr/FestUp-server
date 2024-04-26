from sqlalchemy import Column, String, Text, Integer, Date, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuario'
    username = Column(String, primary_key=True)
    password = Column(LargeBinary)
    email = Column(String)
    nombre = Column(String)

    #asistencias = relationship("UsuarioAsistente")


class Cuadrilla(Base):
    __tablename__ = 'cuadrilla'
    nombre = Column(String, primary_key=True)
    descripcion = Column(Text)
    lugar = Column(String)

    #asistentes = relationship("CuadrillaAsistente")


class CuadrillaAsistente(Base):
    __tablename__ = 'cudarillaAsistente'
    nombre = Column(String, ForeignKey('cuadrilla.nombre'), primary_key=True)
    id = Column(Integer, ForeignKey('evento.id'), primary_key=True)

    #cuadrilla = relationship("Cuadrilla", overlaps="asistentes")
    #evento = relationship("Evento")

class Evento(Base):
    __tablename__ = 'evento'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    fecha = Column(Date)
    numeroAsistentes = Column(Integer)
    descripcion = Column(Text)
    localizacion = Column(String)

class Integrante(Base):
    __tablename__ = 'integrante'
    username = Column(String, ForeignKey('usuario.username'), primary_key=True)
    nombre = Column(String, ForeignKey('cuadrilla.nombre'), primary_key=True)

class Seguidores(Base):
    __tablename__ = 'seguidores'
    siguiendo = Column(String, ForeignKey('usuario.username'), primary_key=True)
    seguido = Column(String, ForeignKey('usuario.username'), primary_key=True)

class UsuarioAsistente(Base):
    __tablename__ = 'usuarioAsistente'
    username = Column(String, ForeignKey('usuario.username'), primary_key=True)
    id = Column(Integer, ForeignKey('evento.id'), primary_key=True)

    #usuario = relationship("User", overlaps="asistencias")
    #evento = relationship("Evento")