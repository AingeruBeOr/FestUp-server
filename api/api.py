from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import crud
import database as db
import api_models
import bcrypt
from fastapi.security import OAuth2PasswordRequestFormStrict
from utils import get_verified_current_user, create_access_token, CREDENTIALS_EXCEPTION, create_refresh_token, TokenResponse, decode_token, OAuth2RefreshTokenForm


app = FastAPI()

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



# ---------------------------  CUADRILLA ------------------------------

@app.get("/getCuadrillas", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_cuadrillas(db: Session = Depends(db.get_database)):
    return crud.get_cuadrillas(db)


# ---------------------------  CUADRILLA ASISTENTE ------------------------------

@app.get("/getCuadrillasAsistentes", response_model=list[api_models.CuadrillaAsistente], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_cuadrillas_asistentes(db: Session = Depends(db.get_database)):
    return crud.get_cuadrillas_asistentes(db)


# ---------------------------  EVENTO ------------------------------

@app.get("/getEventos", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Eventos"])
async def get_eventos(db: Session = Depends(db.get_database)):
    return crud.get_eventos(db)

# ---------------------------  INTEGRANTE ------------------------------
@app.get("/getIntegrantes", response_model=list[api_models.Integrante], status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def get_integrantes(db: Session = Depends(db.get_database)):
    return crud.get_integrantes(db)

# ---------------------------  SEGUIDORES ------------------------------

@app.get("/getSeguidores", response_model=list[api_models.Seguidores], status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def get_seguidores(db: Session = Depends(db.get_database)):
    return crud.get_seguidores(db)