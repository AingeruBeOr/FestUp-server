from sqlalchemy.orm import Session
from sqlalchemy.engine import row
from dbClasses import Usuario, UsuarioAsistente, Cuadrilla, CuadrillaAsistente, Evento, Integrante, Seguidores
import api_models 
import datetime

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
        db_user = Usuario(username=user.username, password=user.hashed_password(), email=user.email, nombre=user.nombre)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

def get_cuadrillas_usuario (db: Session, username: str)-> list[row]:
    return db.query(Cuadrilla).join(Integrante).filter(Integrante.username==username).all()

def get_seguidos_usuario (db: Session, username: str)-> list[row]:
    # hay que expecificarle de cual de los dos queremos los Usuarios (en este caso seguidos)
    return db.query(Usuario).join(Seguidores, Seguidores.seguido == Usuario.username).filter(Seguidores.siguiendo == username).all()
    
def get_seguidores_usuario (db: Session, username: str)-> list[row]:
    # hay que expecificarle de cual de los dos queremos los Usuarios (en este caso siguiendo)
    return db.query(Usuario).join(Seguidores, Seguidores.siguiendo == Usuario.username).filter(Seguidores.seguido == username).all()
    


# ---------------------------  USUARIO ASISTENTE ------------------------------

def get_usuarios_asistentes(db: Session) -> list[row]:
    return db.query(UsuarioAsistente).all()


def get_usuario_asistente(db: Session, usuarioAsistente: api_models.UsuarioAsistente) -> UsuarioAsistente | None:
    return db.query(UsuarioAsistente).filter((UsuarioAsistente.username == usuarioAsistente.username) & (UsuarioAsistente.id == usuarioAsistente.id)).first()


def insert_usuario_asistente(db: Session, usuarioAsistente: api_models.UsuarioAsistente) -> UsuarioAsistente | None:
    if get_usuario_asistente(db, usuarioAsistente):
        return None
    else:
        db_usuario_asistente= UsuarioAsistente(username=usuarioAsistente.username, id=usuarioAsistente.id)
        db.add(db_usuario_asistente)
        db.commit()
        db.refresh(db_usuario_asistente)
        return db_usuario_asistente

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

# ---------------------------  CUADRILLA ------------------------------

def get_cuadrillas(db: Session) -> list[row]:
    return db.query(Cuadrilla).all()

def get_cuadrilla_data(db: Session, nombre_cuadrilla: str) -> Cuadrilla | None:
    return db.query(Cuadrilla).filter((Cuadrilla.nombre == nombre_cuadrilla)).first()

def insert_cuadrilla(db: Session, cuadrilla: api_models.Cuadrilla) -> Cuadrilla | None:
    if get_cuadrilla_data(db, cuadrilla.nombre):
        return None
    else:
        db_cuadrilla = Cuadrilla(nombre=cuadrilla.nombre, descripcion=cuadrilla.descripcion, lugar=cuadrilla.lugar)
        db.add(db_cuadrilla)
        db.commit()
        db.refresh(db_cuadrilla)
        return db_cuadrilla


# ---------------------------  CUADRILLA ASISTENTE ------------------------------

def get_cuadrillas_asistentes(db: Session) -> list[row]:
    return db.query(CuadrillaAsistente).all()

def get_eventos_from_cuadrilla(db: Session, nombre_cuadrilla: str) -> list[Evento]:
    return db.query(Evento).join(CuadrillaAsistente).filter(CuadrillaAsistente.nombre==nombre_cuadrilla).all()

def get_future_eventos_from_cuadrilla(db: Session, nombre_cuadrilla: str) -> list[Evento]:
    return db.query(Evento).join(CuadrillaAsistente).filter((CuadrillaAsistente.nombre==nombre_cuadrilla) & (Evento.fecha >= datetime.date.today())).all()

def get_cuadrillas_from_evento(db: Session, eventoId: int) -> list[Cuadrilla]:
    return db.query(Cuadrilla).join(CuadrillaAsistente).filter(CuadrillaAsistente.id==eventoId).all()

def is_cuadrilla_asistente(db: Session, cuadrillaAsistente: api_models.CuadrillaAsistente) -> bool:
    return db.query(CuadrillaAsistente).filter((CuadrillaAsistente.nombre == cuadrillaAsistente.nombre) & (CuadrillaAsistente.id == CuadrillaAsistente.id)).first()

def insert_cuadrilla_asistente(db: Session, cuadrillaAsistente: api_models.CuadrillaAsistente) -> CuadrillaAsistente | None:
    if is_cuadrilla_asistente(db, cuadrillaAsistente):
        return None
    else:
        db_cuadrilla_asistente = CuadrillaAsistente(nombre=cuadrillaAsistente.nombre, id=cuadrillaAsistente.id)
        db.add(db_cuadrilla_asistente)
        db.commit()
        db.refresh(db_cuadrilla_asistente)
        return db_cuadrilla_asistente


# ---------------------------  EVENTO ------------------------------

def get_eventos(db: Session) -> list[row]:
    return db.query(Evento).all()

def get_evento_data_from_id(db: Session, eventoId: int) -> Evento | None:
    return db.query(Evento).filter(Evento.id == eventoId).first()

def insert_evento(db: Session, evento: api_models.Evento) -> Evento | None:
    if get_evento_data_from_id(db, evento.id):
        return None
    else:
        db_evento = Evento(id=evento.id, nombre=evento.nombre, fecha=evento.fecha, numeroAsistentes=evento.numeroAsistentes, descripcion=evento.descripcion, localizacion=evento.localizacion)
        db.add(db_evento)
        db.commit()
        db.refresh(db_evento)
        return db_evento


# ---------------------------  INTEGRANTE ------------------------------

def get_integrantes(db: Session) -> list[row]:
    return db.query(Integrante).all()

def get_integrante_from_username(db: Session, username: str, cuadrilla: str) -> Integrante | None:
    return db.query(Integrante).filter((Integrante.username == username) & (Integrante.nombre == cuadrilla)).first()

def insert_integrante(db: Session, integrante: api_models.Integrante) -> Integrante | None:
    if get_integrante_from_username(db, integrante.username, integrante.nombre):
        return None
    else:
        db_integrante = Integrante(username=integrante.username, nombre=integrante.nombre)
        db.add(db_integrante)
        db.commit()
        db.refresh(db_integrante)
        return db_integrante

# ---------------------------  SEGUIDORES ------------------------------

def get_seguidores(db: Session) -> list[row]:
    return db.query(Seguidores).all()

def is_already_following(db: Session, seguidores: api_models.Seguidores) -> bool:
    return db.query(Seguidores).filter((Seguidores.siguiendo == seguidores.siguiendo) & (Seguidores.seguido == seguidores.seguido)).first() is not None

def insert_seguidores(db: Session, seguidores: api_models.Seguidores) -> Seguidores | None:
    if is_already_following(db, seguidores):
        return None
    else: 
        db_seguidores = Seguidores(siguiendo=seguidores.siguiendo, seguido=seguidores.seguido)
        db.add(db_seguidores)
        db.commit()
        db.refresh(db_seguidores)
        return db_seguidores
