from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestFormStrict
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import bcrypt
import os
import api_models
from utils import get_verified_current_user, create_access_token, CREDENTIALS_EXCEPTION, create_refresh_token, TokenResponse, decode_token, OAuth2RefreshTokenForm
import crud
import database as db


app = FastAPI()

if not os.path.exists('./userProfileImages'): os.mkdir('./userProfileImages')
app.mount("/userProfileImages", StaticFiles(directory="userProfileImages"), name="userProfileImages")

if not os.path.exists('./cuadrillaProfileImages'): os.mkdir('./cuadrillaProfileImages')
app.mount("/cuadrillaProfileImages", StaticFiles(directory="cuadrillaProfileImages"), name="cuadrillaProfileImages")

if not os.path.exists('./eventoImages'): os.mkdir('./eventoImages')
app.mount("/eventoImages", StaticFiles(directory="eventoImages"), name="eventoImages")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url='/docs')



# ---------------------------  USER ------------------------------

@app.get("/getUsers", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_users(db: Session = Depends(db.get_database), current_user: str = Depends(get_verified_current_user)):
    return crud.get_users(db)

@app.post("/iniciarSesion", response_model=TokenResponse, status_code=status.HTTP_200_OK, tags=['Usuarios'])
async def identificar(form_data: OAuth2PasswordRequestFormStrict = Depends(), db: Session = Depends(db.get_database)):
    hashed_password = crud.get_user_password(db, username=form_data.username)

    if hashed_password is None or not bcrypt.checkpw(form_data.password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=404, detail="User or password is not correct.")

    access_token, expire_in_seconds = create_access_token(data={"sub": form_data.username})
    return {
        "token_type": "bearer",
        "expires_in": expire_in_seconds,
        "access_token": access_token,
        'refresh_token': create_refresh_token(data={"sub": form_data.username}),
    }
    
@app.post("/refresh", tags=['Tokens'], response_model=TokenResponse, status_code=status.HTTP_200_OK,
          responses={401: {"description": "Could not validate credentials."},403: {"description": "This user does not exist anymore."}})
async def refresh(form_data: OAuth2RefreshTokenForm = Depends(), db: Session = Depends(db.get_database)):
    try:
        token = form_data.refresh_token
        username = decode_token(token).get('sub')

        # Validate email
        if crud.get_user_password(db, username=username):
            # Create and return token
            access_token, expire_in_seconds = create_access_token(data={"sub": username})
            return {
                "token_type": "bearer",
                "expires_in": expire_in_seconds,
                "access_token": access_token,
                'refresh_token': create_refresh_token(data={"sub": username}),
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This user does not exist.")

    except Exception:
        raise CREDENTIALS_EXCEPTION


@app.post("/createUser", tags=["Usuarios"],
          response_model=api_models.Usuario, status_code=status.HTTP_201_CREATED,
          responses={400: {"description": "Password is not valid."}, 409: {"description": "Username already registered."}}, )
async def create_user(user: api_models.UsuarioAuth, db: Session = Depends(db.get_database)):
    #if len(user.password) < 5:
    #    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not valid.")

    if not (db_user := crud.create_user(db=db, user=user)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return db_user

@app.get("/getCuadrillasUsuario", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_cuadrillas_usuario(username: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_cuadrillas_usuario(db, username)

@app.get("/getSeguidosUsuario", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_seguidos_usuario(username: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_seguidos_usuario(db, username)

@app.get("/getSeguidoresUsuario", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_seguidores_usuario(username: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_seguidores_usuario(db, username)


# ---------------------------  USUARIO ASISTENTE ------------------------------

@app.get("/getUsuariosAsistentes", response_model=list[api_models.UsuarioAsistente], status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def get_usuarios_asistentes(db: Session = Depends(db.get_database)):
    return crud.get_usuarios_asistentes(db)

@app.post("/insertUsuarioAsistente", response_model=api_models.UsuarioAsistente, status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def insert_usuario_asistente(usuarioAsistente: api_models.UsuarioAsistente, db: Session = Depends(db.get_database)):
    if not (db_asistente := crud.insert_usuario_asistente(db, usuarioAsistente)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese usuario ya está apuntado al evento")
    return db_asistente

@app.get("/getUsuariosAsistentesEvento", response_model=list[str], status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def get_usuarios_asistentes_evento(eventoId: int, db: Session = Depends(db.get_database)):
    return crud.get_usuarios_asistentes_evento(db, eventoId)

@app.get("/getEventosUsuarioAsistente", response_model=list[int], status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def get_eventos_usuario_asistente(username: str, db: Session = Depends(db.get_database)):
    return crud.get_eventos_usuario_asistente(db, username)

@app.get("/getEventosUsuarioAsistenteData", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def get_eventos_usuario_asistentes_data(username: str, db: Session = Depends(db.get_database)):
    return crud.get_eventos_usuario_asistentes_data(db, username)

@app.get("/getFutureEventosUsuarioAsistente", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def get_future_eventos_usuario_asistente(username: str, db: Session = Depends(db.get_database)):
    return crud.get_future_eventos_usuario_asistentes_data(db, username)


@app.post("/deleteUsuarioAsistente", response_model=api_models.UsuarioAsistente, status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def delete_usuario_asistente(usuarioAsistente: api_models.UsuarioAsistente, db: Session = Depends(db.get_database)):
    if not (usuarioAsistente := crud.get_usuario_asistente(db, usuarioAsistente)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese usuario no asiste a ese evento")

    return crud.delete_usuario_asistente(db, usuarioAsistente)

# ---------------------------  CUADRILLA ------------------------------

@app.get("/getCuadrillas", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_cuadrillas(db: Session = Depends(db.get_database)):
    return crud.get_cuadrillas(db)

@app.get("/getCuadrillaData", response_model=api_models.Cuadrilla, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_cuadrilla_data(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_cuadrilla_data(db, nombre)

@app.post("/insertCuadrilla", response_model=api_models.Cuadrilla, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def insert_cuadrilla(cuadrilla: api_models.Cuadrilla, db: Session = Depends(db.get_database)):
    if not (db_cuadrilla := crud.insert_cuadrilla(db, cuadrilla)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esa cuadrilla ya existe")
    return db_cuadrilla

@app.post("/deleteCuadrilla", response_model=api_models.Cuadrilla, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def delete_cuadrilla(nombre: str, db: Session = Depends(db.get_database)):
    if not (cuadrilla := crud.get_cuadrilla_data(db, nombre)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esa cuadrilla no existe")

    return crud.delete_cuadrilla(db, cuadrilla)

# ---------------------------  CUADRILLA ASISTENTE ------------------------------

@app.get("/getCuadrillasAsistentes", response_model=list[api_models.CuadrillaAsistente], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_cuadrillas_asistentes(db: Session = Depends(db.get_database)):
    return crud.get_cuadrillas_asistentes(db)

@app.get("/getEventosFromCuadrilla", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_eventos_from_cuadrilla(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_eventos_from_cuadrilla(db, nombre)

@app.get("/getFutureEventosFromCuadrilla", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_future_eventos_from_cuadrilla(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_future_eventos_from_cuadrilla(db, nombre)

@app.get("/getCuadrillasFromEvento", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_cuadrillas_from_evento(eventoId: int, db: Session = Depends(db.get_database)):
    return crud.get_cuadrillas_from_evento(db, eventoId)

@app.post("/insertCuadrillaAsistente", response_model=api_models.CuadrillaAsistente, status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def insert_cuadrilla_asistente(cuadrillaAsistente: api_models.CuadrillaAsistente, db: Session = Depends(db.get_database)):
    if not (db_cuadrilla_asistente := crud.insert_cuadrilla_asistente(db, cuadrillaAsistente)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esa cuadrilla ya está apuntada al evento")
    return db_cuadrilla_asistente

@app.post("/deleteCuadrillaAsistente", response_model=api_models.CuadrillaAsistente, status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def delete_cuadrilla_asistente(cuadrillaAsistente: api_models.CuadrillaAsistente, db: Session = Depends(db.get_database)):
    if not (cuadrillaAsistente := crud.get_cuadrilla_asistente(db, cuadrillaAsistente)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esa cuadrilla no asiste a ese evento")

    return crud.delete_cuadrilla_asistente(db, cuadrillaAsistente)


# ---------------------------  EVENTO ------------------------------

@app.get("/getEventos", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Eventos"])
async def get_eventos(db: Session = Depends(db.get_database)):
    return crud.get_eventos(db)

@app.get("/getEventoDataFromId", response_model=api_models.Evento, status_code=status.HTTP_200_OK, tags=["Eventos"])
async def get_evento_data_from_id(eventoId: int, db: Session = Depends(db.get_database)):
    return crud.get_evento_data_from_id(db, eventoId)

@app.post("/insertEvento", response_model=api_models.Evento, status_code=status.HTTP_200_OK, tags=["Eventos"])
async def insert_evento(evento: api_models.Evento, db: Session = Depends(db.get_database)):
    if not (db_evento := crud.insert_evento(db, evento)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese evento ya existe")
    return db_evento

@app.post("/deleteEvento", response_model=api_models.Evento, status_code=status.HTTP_200_OK, tags=["Eventos"])
async def delete_evento(eventoId: int, db: Session = Depends(db.get_database)):
    if not (evento := crud.get_evento_data_from_id(db, eventoId)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese evento no existe")

    return crud.delete_evento(db, evento)


# ---------------------------  INTEGRANTE ------------------------------
@app.get("/getIntegrantes", response_model=list[api_models.Integrante], status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def get_integrantes(db: Session = Depends(db.get_database)):
    return crud.get_integrantes(db)

@app.post("/insertIntegrante", response_model=api_models.Integrante, status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def insert_integrante(integrante: api_models.Integrante, db: Session = Depends(db.get_database)):
    if not (db_integrante := crud.insert_integrante(db, integrante)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"'{integrante.username}' ya está en '{integrante.nombre}'")
    return db_integrante

@app.post("/deleteIntegrante", response_model=api_models.Integrante, status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def delete_integrante(integrante: api_models.Integrante, db: Session = Depends(db.get_database)):
    if not (integrante := crud.get_integrante_from_username(db, integrante.username, integrante.nombre)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese integrante no pertenece a esa cuadrilla")

    return crud.delete_integrante(db, integrante)


# ---------------------------  SEGUIDORES ------------------------------

@app.get("/getSeguidores", response_model=list[api_models.Seguidores], status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def get_seguidores(db: Session = Depends(db.get_database)):
    return crud.get_seguidores(db)

@app.post("/insertSeguidores", response_model=api_models.Seguidores, status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def insert_seguidores(seguidores: api_models.Seguidores, db: Session = Depends(db.get_database)):
    if not (db_seguidores := crud.insert_seguidores(db, seguidores)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"'{seguidores.siguiendo}' ya sigue a '{seguidores.seguido}'")
    return db_seguidores


@app.post("/deleteSeguidor", response_model=api_models.Seguidores, status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def delete_seguidor(seguidor: api_models.Seguidores, db: Session = Depends(db.get_database)):
    if not (seguidor := crud.get_seguidor(db, seguidor)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese usuario no sigue a ese otro usuario")

    return crud.delete_seguidor(db, seguidor)
