import bcrypt
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy import Text


class UsuarioAsistente(BaseModel):
    username: str
    id: int

    class Config:
        orm_mode = True

class UsuarioAsistenteCreate(UsuarioAsistente):
    pass

class Usuario(BaseModel):
    username: str
    email: str
    nombre: str
    fechaNacimiento: str


    class Config:
        orm_mode = True

# Inherits Usuario properties
class UsuarioAuth(Usuario):
    password: str

    def hashed_password(self) -> bytes:
        bytePwd = self.password.encode('utf-8')

        # Hash password with salt
        return bcrypt.hashpw(bytePwd, bcrypt.gensalt())

class Cuadrilla(BaseModel):
    nombre: str
    descripcion: str
    lugar: str
    accessToken: str

    class Config:
        orm_mode = True


class CuadrillaAsistente(BaseModel):
    nombre: str
    id: int

    class Config:
        orm_mode = True



class Evento(BaseModel):
    id: str # TODO cambiar cuando se genere en el server
    nombre: str
    fecha: str
    numeroAsistentes: int
    descripcion: str
    localizacion: str

    class Config:
        orm_mode = True



class Integrante(BaseModel):
    username: str
    nombre: str

    class Config:
        orm_mode = True



class Seguidores(BaseModel):
    siguiendo: str
    seguido: str

    class Config:
        orm_mode = True
