from sqlalchemy.orm import Session
from sqlalchemy.engine import row
from dbClasses import Usuario, UsuarioAsistente, Cuadrilla, CuadrillaAsistente, Evento, Integrante, Seguidores
import api_models 
import datetime
import secrets

# ---------------------------  USER ------------------------------

def get_users (db: Session) -> list[row]:
    return db.query(Usuario).all()

def get_user_password(db: Session, username: str) -> bytes | None:
    result = db.query(Usuario.password).filter(Usuario.username == username).first()
    return result.password if result else None

def get_user (db: Session, username: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.username == username).first()

def create_user (db: Session, user: api_models.UsuarioAuth) -> Usuario | None:
    if get_user(db, username=user.username):
        return None
    else:
        db_user = Usuario(
            username=user.username, 
            password=user.hashed_password(), 
            email=user.email, 
            nombre=user.nombre,
            fechaNacimiento=user.fechaNacimiento,
            telefono=user.telefono
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

def update_user(db: Session, user: api_models.Usuario) -> Usuario | None:
    user_db = get_user(db, username=user.username)
    if user_db == None:
        return None
    else:
        user_db.email = user.email
        user_db.fechaNacimiento = user.fechaNacimiento
        user_db.nombre = user.nombre
        user_db.telefono = user.telefono
        db.commit()
        return user_db

"""
def get_cuadrillas_usuario (db: Session, username: str)-> list[row]:
    return db.query(Cuadrilla).join(Integrante).filter(Integrante.username==username).all()

def get_seguidos_usuario (db: Session, username: str)-> list[row]:
    # hay que expecificarle de cual de los dos queremos los Usuarios (en este caso seguidos)
    return db.query(Usuario).join(Seguidores, Seguidores.seguido == Usuario.username).filter(Seguidores.siguiendo == username).all()
    
def get_seguidores_usuario (db: Session, username: str)-> list[row]:
    # hay que expecificarle de cual de los dos queremos los Usuarios (en este caso siguiendo)
    return db.query(Usuario).join(Seguidores, Seguidores.siguiendo == Usuario.username).filter(Seguidores.seguido == username).all()
    
"""

# ---------------------------  USUARIO ASISTENTE ------------------------------

def get_usuarios_asistentes(db: Session) -> list[row]:
    return db.query(UsuarioAsistente).all()


def get_usuario_asistente(db: Session, usuarioAsistente: api_models.UsuarioAsistente) -> UsuarioAsistente | None:
    return db.query(UsuarioAsistente).filter((UsuarioAsistente.username == usuarioAsistente.username) & (UsuarioAsistente.id == usuarioAsistente.idEvento)).first()


def insert_usuario_asistente(db: Session, usuarioAsistente: api_models.UsuarioAsistente) -> UsuarioAsistente | None:
    if get_usuario_asistente(db, usuarioAsistente):
        return None
    else:
        db_usuario_asistente= UsuarioAsistente(username=usuarioAsistente.username, id=usuarioAsistente.idEvento)
        db.add(db_usuario_asistente)
        db.commit()
        db.refresh(db_usuario_asistente)
        return db_usuario_asistente

"""
def get_usuarios_asistentes_evento(db: Session, eventoId: int) -> list[str]:
    usernames = db.query(UsuarioAsistente.username).filter(UsuarioAsistente.id==eventoId).all()
    return [username[0] for username in usernames]

def get_eventos_usuario_asistente(db: Session, username: str) -> list[int]:
    ids = db.query(UsuarioAsistente.id).filter(UsuarioAsistente.username==username).all()
    return [id[0] for id in ids]

def get_eventos_usuario_asistentes_data(db: Session, username: str) -> list[Evento]:
    return db.query(Evento).join(UsuarioAsistente).filter(UsuarioAsistente.username==username).all()

def get_future_eventos_usuario_asistentes_data(db: Session, username: str) -> list[Evento]:
    return db.query(Evento).join(UsuarioAsistente).filter((UsuarioAsistente.username==username) & (Evento.fecha >= datetime.date.today())).all()
"""

def delete_usuario_asistente(db: Session, usuarioAsistente: api_models.UsuarioAsistente) -> UsuarioAsistente | None:
    db.delete(usuarioAsistente)
    db.commit()
    return usuarioAsistente
# ---------------------------  CUADRILLA ------------------------------

def get_cuadrillas(db: Session) -> list[row]:
    return db.query(Cuadrilla).all()

def get_cuadrilla(db: Session, nombre_cuadrilla: str) -> Cuadrilla | None:
    return db.query(Cuadrilla).filter((Cuadrilla.nombre == nombre_cuadrilla)).first()

def insert_cuadrilla(db: Session, cuadrilla: api_models.Cuadrilla) -> Cuadrilla | None:
    if get_cuadrilla(db, cuadrilla.nombre):
        return None
    else:
        token = ''.join(secrets.choice('0123456789') for _ in range(8))
        db_cuadrilla = Cuadrilla(nombre=cuadrilla.nombre, descripcion=cuadrilla.descripcion, lugar=cuadrilla.lugar, accessToken= token)
        db.add(db_cuadrilla)
        db.commit()
        db.refresh(db_cuadrilla)
        return db_cuadrilla

def delete_cuadrilla(db: Session, cuadrilla: api_models.Cuadrilla) -> Cuadrilla | None:
    db.delete(cuadrilla)
    db.commit()
    return cuadrilla

def get_cuadrilla_access_token(db: Session, nombre_cuadrilla: str) -> str :
    cuadrilla = db.query(Cuadrilla).filter(Cuadrilla.nombre == nombre_cuadrilla).first()
    if cuadrilla:
        return cuadrilla.accessToken
    else:
        return "Esa cuadrilla no existe"

"""
def get_usuarios_cuadrilla(db: Session, nombre_cuadrilla: str) -> list[Usuario]:
    return db.query(Usuario).join(Integrante).filter(Integrante.nombre==nombre_cuadrilla).all()
"""
# ---------------------------  CUADRILLA ASISTENTE ------------------------------

def get_cuadrillas_asistentes(db: Session) -> list[row]:
    return db.query(CuadrillaAsistente).all()

"""
def get_eventos_from_cuadrilla(db: Session, nombre_cuadrilla: str) -> list[Evento]:
    return db.query(Evento).join(CuadrillaAsistente).filter(CuadrillaAsistente.nombre==nombre_cuadrilla).all()

def get_future_eventos_from_cuadrilla(db: Session, nombre_cuadrilla: str) -> list[Evento]:
    return db.query(Evento).join(CuadrillaAsistente).filter((CuadrillaAsistente.nombre==nombre_cuadrilla) & (Evento.fecha >= datetime.date.today())).all()

def get_cuadrillas_from_evento(db: Session, eventoId: int) -> list[Cuadrilla]:
    return db.query(Cuadrilla).join(CuadrillaAsistente).filter(CuadrillaAsistente.id==eventoId).all()


def is_cuadrilla_asistente(db: Session, cuadrillaAsistente: api_models.CuadrillaAsistente) -> bool:
    return db.query(CuadrillaAsistente).filter((CuadrillaAsistente.nombre == cuadrillaAsistente.nombre) & (CuadrillaAsistente.id == CuadrillaAsistente.id)).first()
"""
def insert_cuadrilla_asistente(db: Session, cuadrillaAsistente: api_models.CuadrillaAsistente) -> CuadrillaAsistente | None:
    if get_cuadrilla_asistente(db, cuadrillaAsistente):
        return None
    else:
        db_cuadrilla_asistente = CuadrillaAsistente(nombre=cuadrillaAsistente.nombre, id=cuadrillaAsistente.id)
        db.add(db_cuadrilla_asistente)
        db.commit()
        db.refresh(db_cuadrilla_asistente)
        return db_cuadrilla_asistente

def get_cuadrilla_asistente(db: Session, cuadrillaAsistente: api_models.CuadrillaAsistente) -> CuadrillaAsistente | None:
    return db.query(CuadrillaAsistente).filter((CuadrillaAsistente.nombre == cuadrillaAsistente.nombre) & (CuadrillaAsistente.id == cuadrillaAsistente.id)).first()


def delete_cuadrilla_asistente(db: Session, cuadrillaAsistente: api_models.CuadrillaAsistente) -> CuadrillaAsistente | None:
    db.delete(cuadrillaAsistente)
    db.commit()
    return cuadrillaAsistente

# ---------------------------  EVENTO ------------------------------

def get_eventos(db: Session) -> list[row]:
    return db.query(Evento).all()

def get_evento(db: Session, eventoId: str) -> Evento | None:
    return db.query(Evento).filter(Evento.id == eventoId).first()

def insert_evento(db: Session, evento: api_models.Evento) -> Evento | None:
    '''if get_evento(db, evento.id):
        return None
    else:'''
    db_evento = Evento(nombre=evento.nombre, fecha=evento.fecha, descripcion=evento.descripcion, localizacion=evento.localizacion)
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def delete_evento(db: Session, evento: api_models.Evento) -> Evento | None:
    db.delete(evento)
    db.commit()
    return evento

# ---------------------------  INTEGRANTE ------------------------------

def get_integrantes(db: Session) -> list[row]:
    return db.query(Integrante).all()

def get_integrante(db: Session, integrante: api_models.Integrante) -> Integrante | None:
    return db.query(Integrante).filter((Integrante.username == integrante.username) & (Integrante.nombre == integrante.nombre)).first()

def insert_integrante(db: Session, integrante: api_models.Integrante) -> Integrante | None:
    if get_integrante(db, integrante):
        return None
    else:
        db_integrante = Integrante(username=integrante.username, nombre=integrante.nombre)
        db.add(db_integrante)
        db.commit()
        db.refresh(db_integrante)
        return db_integrante

def delete_integrante(db: Session, integrante: api_models.Integrante) -> Integrante | None:
    db.delete(integrante)
    db.commit()
    return integrante

# ---------------------------  SEGUIDORES ------------------------------

def get_seguidores(db: Session) -> list[row]:
    return db.query(Seguidores).all()

"""
def is_already_following(db: Session, seguidores: api_models.Seguidores) -> bool:
    return db.query(Seguidores).filter((Seguidores.siguiendo == seguidores.siguiendo) & (Seguidores.seguido == seguidores.seguido)).first() is not None

"""
def insert_seguidores(db: Session, seguidores: api_models.Seguidores) -> Seguidores | None:
    if get_seguidor(db, seguidores):
        return None
    else: 
        db_seguidores = Seguidores(siguiendo=seguidores.seguidor, seguido=seguidores.seguido)
        db.add(db_seguidores)
        db.commit()
        db.refresh(db_seguidores)
        return db_seguidores

def get_seguidor(db: Session, seguidor: api_models.Seguidores) -> Seguidores| None:
    return db.query(Seguidores).filter((Seguidores.siguiendo == seguidor.seguidor) & (Seguidores.seguido == seguidor.seguido)).first()

def delete_seguidor(db: Session, seguidor: api_models.Seguidores) -> Seguidores | None:
    db.delete(seguidor)
    db.commit()
    return seguidor
