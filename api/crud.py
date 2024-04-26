from sqlalchemy.orm import Session
from sqlalchemy.engine import row
from dbClasses import Usuario, UsuarioAsistente, Cuadrilla, CuadrillaAsistente, Evento, Integrante, Seguidores
import api_models 

# ---------------------------  USER ------------------------------

def get_users(db: Session) -> list[row]:
    return db.query(Usuario).all()

def get_user_password(db: Session, username: str) -> bytes | None:
    result = db.query(Usuario.password).filter(Usuario.username == username).first()
    return result.password if result else None

def get_user(db: Session, username: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.username == username).first()

def create_user(db: Session, user: api_models.UsuarioAuth) -> Usuario | None:
    if get_user(db, username=user.username):
        return None
    else:
        db_user = Usuario(username=user.username, password=user.hashed_password(), email=user.email, nombre=user.nombre)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user



# ---------------------------  USUARIO ASISTENTE ------------------------------

def get_users_asistentes(db: Session) -> list[row]:
    return db.query(UsuarioAsistente).all()


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
