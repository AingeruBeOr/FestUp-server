from sqlalchemy.orm import Session
from sqlalchemy.engine import row
from dbClasses import Usuario, UsuarioAsistente, Cuadrilla, CuadrillaAsistente, Evento, Integrante, Seguidores
import api_models 

# ---------------------------  USER ------------------------------

def get_users (db: Session) -> list[row]:
    return db.query(Usuario).all()

def get_user_password (db: Session, username: str) -> bytes | None:
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

# ---------------------------  CUADRILLA ------------------------------

def get_cuadrillas(db: Session) -> list[row]:
    return db.query(Cuadrilla).all()


# ---------------------------  CUADRILLA ASISTENTE ------------------------------

def get_cuadrillas_asistentes(db: Session) -> list[row]:
    return db.query(CuadrillaAsistente).all()

# ---------------------------  EVENTO ------------------------------

def get_eventos(db: Session) -> list[row]:
    return db.query(Evento).all()


# ---------------------------  INTEGRANTE ------------------------------

def get_integrantes(db: Session) -> list[row]:
    return db.query(Integrante).all()

# ---------------------------  SEGUIDORES ------------------------------

def get_seguidores(db: Session) -> list[row]:
    return db.query(Seguidores).all()
