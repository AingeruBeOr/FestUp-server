from fastapi import FastAPI, Depends, status, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestFormStrict
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import firebase_admin
from firebase_admin import credentials, messaging
import bcrypt
from unidecode import unidecode
import os
import random
import api_models
import converters
from utils import get_verified_current_user, create_access_token, CREDENTIALS_EXCEPTION, create_refresh_token, TokenResponse, decode_token, OAuth2RefreshTokenForm, apiDateStrToDatabaseStr
import crud
import database as db
from api_models import Message, FirebaseClientToken


app = FastAPI()

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)


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


@app.post("/auth/iniciarSesion", response_model=TokenResponse, status_code=status.HTTP_200_OK, tags=['Usuarios'])
async def identificar(form_data: OAuth2PasswordRequestFormStrict = Depends(), db: Session = Depends(db.get_database)):
    hashed_password = crud.get_user_password(db, username=form_data.username)

    if hashed_password is None or not bcrypt.checkpw(form_data.password.encode('utf-8'), hashed_password):
        raise HTTPException(status_code=404, detail="User or password is not correct.")

    print(f"login: {form_data.username}")
    access_token, expire_in_seconds = create_access_token(data={"sub": form_data.username})
    print(f"access_token: {access_token}")
    return {
        "token_type": "bearer",
        "expires_in": expire_in_seconds,
        "access_token": access_token,
        'refresh_token': create_refresh_token(data={"sub": form_data.username}),
    }

@app.post("/auth/refresh", tags=['Tokens'], response_model=TokenResponse, status_code=status.HTTP_200_OK,
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

    print(f"create: {user.nombre}")
    user.fechaNacimiento = apiDateStrToDatabaseStr(user.fechaNacimiento)
    if not (db_user := crud.create_user(db=db, user=user)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return converters.apiUsuarioFromDBUsuario(db_user)

"""
@app.get("/getCuadrillasUsuario", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_cuadrillas_usuario(username: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_cuadrillas_usuario(db, username)

@app.get("/getSeguidosUsuario", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_seguidos_usuario(username: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_seguidos_usuario(db, username)

@app.get("/getSeguidoresUsuario", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_seguidores_usuario(username: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_seguidores_usuario(db, username)

"""
@app.get("/getUsers", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_users(db: Session = Depends(db.get_database)):
    db_usuarios = crud.get_users(db)

    usuarios_to_return = [ 
        converters.apiUsuarioFromDBUsuario(usuario) 
        for usuario in db_usuarios
    ]
    return usuarios_to_return

@app.put("/setUserProfileImage", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def insert_usuario_image(image: UploadFile):
    print('Saving user profile image')
    with open(f'./userProfileImages/{image.filename}', 'wb') as f:
        f.write(await image.read())

@app.get("/getUser", response_model=api_models.Usuario, status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def get_user(username: str, db: Session = Depends(db.get_database), current_user: str = Depends(get_verified_current_user)):
    user = crud.get_user(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return converters.apiUsuarioFromDBUsuario(user)  

@app.post("/editUser", response_model=api_models.Usuario, status_code=status.HTTP_200_OK, tags=["Usuarios"])
async def edit_user(user: api_models.Usuario, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    updated_user = crud.update_user(db, user)
    return converters.apiUsuarioFromDBUsuario(updated_user)

# ---------------------------  USUARIO ASISTENTE ------------------------------

@app.get("/getUsuariosAsistentes", response_model=list[api_models.UsuarioAsistente], status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def get_usuarios_asistentes(db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    db_asistentes = crud.get_usuarios_asistentes(db)
    asistentes_to_return = [
        converters.apiUsuarioAsistenteFormDBUsuarioAsistente(db_asistente) 
        for db_asistente in db_asistentes
    ]
    return asistentes_to_return

@app.post("/insertUsuarioAsistente", response_model=api_models.UsuarioAsistente, status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def insert_usuario_asistente(usuarioAsistente: api_models.UsuarioAsistente, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    
    if not (db_asistente := crud.insert_usuario_asistente(db, usuarioAsistente)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese usuario ya está apuntado al evento")


    usernameNuevo= db_asistente.username+"2"
    evento= crud.get_evento(db, db_asistente.id)
    
    await send_notification_to_user(usernameNuevo, Message(title="@"+db_asistente.username+" se ha apuntado a un evento!", body=evento.nombre+ ", "+ str(evento.fecha)))

    return converters.apiUsuarioAsistenteFormDBUsuarioAsistente(db_asistente)

"""
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

"""

@app.post("/deleteUsuarioAsistente", response_model=api_models.UsuarioAsistente, status_code=status.HTTP_200_OK, tags=["Usuarios Asistentes"])
async def delete_usuario_asistente(usuarioAsistente: api_models.UsuarioAsistente, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (usuarioAsistente := crud.get_usuario_asistente(db, usuarioAsistente)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese usuario no asiste a ese evento")

    deleted_usuario = crud.delete_usuario_asistente(db, usuarioAsistente)
    return converters.apiUsuarioAsistenteFormDBUsuarioAsistente(deleted_usuario)

# ---------------------------  CUADRILLA ------------------------------

@app.get("/getCuadrillas", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_cuadrillas(db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_cuadrillas(db)

@app.post("/insertCuadrilla", response_model=api_models.Cuadrilla, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def insert_cuadrilla(cuadrilla: api_models.Cuadrilla, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (db_cuadrilla := crud.insert_cuadrilla(db, cuadrilla)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esa cuadrilla ya existe")
    return db_cuadrilla

@app.put("/insertCuadrillaImage", tags=["Cuadrillas"], status_code=status.HTTP_200_OK)
async def insert_cuadrilla_image(image: UploadFile, _: str = Depends(get_verified_current_user)):
    with open(f'./cuadrillaProfileImages/{image.filename}', 'wb') as f:
        f.write(await image.read())

@app.post("/deleteCuadrilla", response_model=api_models.Cuadrilla, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def delete_cuadrilla(nombre: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (cuadrilla := crud.get_cuadrilla(db, nombre)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esa cuadrilla no existe")

    # Delete also profile image
    try:
        os.remove(f'./cuadrillaProfileImages/{cuadrilla.nombre}.png')
    except FileNotFoundError:
        pass
    return crud.delete_cuadrilla(db, cuadrilla)

@app.get("/getCuadrillaAccessToken", response_model=str, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_cuadrilla_access_token(nombre: str,db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_cuadrilla_access_token(db,nombre)


"""
@app.get("/getUsuariosCuadrilla", response_model=list[api_models.Usuario], status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_usuarios_cuadrilla(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_usuarios_cuadrilla(db, nombre)

@app.get("/getCuadrillaData", response_model=api_models.Cuadrilla, status_code=status.HTTP_200_OK, tags=["Cuadrillas"])
async def get_cuadrilla_data(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_cuadrilla_data(db, nombre)
"""

# ---------------------------  CUADRILLA ASISTENTE ------------------------------

@app.get("/getCuadrillasAsistentes", response_model=list[api_models.CuadrillaAsistente], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_cuadrillas_asistentes(db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    cuadrilla_asistentes = crud.get_cuadrillas_asistentes(db)
    return [ 
        converters.apiCuadrillaAsistenteFromDBCuadrillaAsistente(cuadrilla_asistente) 
        for cuadrilla_asistente in cuadrilla_asistentes
    ]

"""
@app.get("/getEventosFromCuadrilla", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_eventos_from_cuadrilla(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_eventos_from_cuadrilla(db, nombre)

@app.get("/getFutureEventosFromCuadrilla", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_future_eventos_from_cuadrilla(nombre: str, db: Session = Depends(db.get_database)):
    return crud.get_future_eventos_from_cuadrilla(db, nombre)

@app.get("/getCuadrillasFromEvento", response_model=list[api_models.Cuadrilla], status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def get_cuadrillas_from_evento(eventoId: int, db: Session = Depends(db.get_database)):
    return crud.get_cuadrillas_from_evento(db, eventoId)

"""

@app.post("/insertCuadrillaAsistente", response_model=api_models.CuadrillaAsistente, status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def insert_cuadrilla_asistente(cuadrillaAsistente: api_models.CuadrillaAsistente, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (db_cuadrilla_asistente := crud.insert_cuadrilla_asistente(db, cuadrillaAsistente)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Esa cuadrilla ya está apuntada al evento")
    return converters.apiCuadrillaAsistenteFromDBCuadrillaAsistente(db_cuadrilla_asistente)

@app.post("/deleteCuadrillaAsistente", response_model=api_models.CuadrillaAsistente, status_code=status.HTTP_200_OK, tags=["Cuadrillas Asistentes"])
async def delete_cuadrilla_asistente(cuadrillaAsistente: api_models.CuadrillaAsistente, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (cuadrillaAsistente := crud.get_cuadrilla_asistente(db, cuadrillaAsistente)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Esa cuadrilla no asiste a ese evento")

    deleted_cuadrilla = crud.delete_cuadrilla_asistente(db, cuadrillaAsistente)
    return converters.apiCuadrillaAsistenteFromDBCuadrillaAsistente(deleted_cuadrilla)


# ---------------------------  EVENTO ------------------------------

@app.get("/getEventos", response_model=list[api_models.Evento], status_code=status.HTTP_200_OK, tags=["Eventos"])
async def get_eventos(db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    db_eventos = crud.get_eventos(db)
    
    eventos_to_return = [converters.apiEventoFromDBEvento(db_evento) for db_evento in db_eventos]
    return eventos_to_return
"""
@app.get("/getEventoDataFromId", response_model=api_models.Evento, status_code=status.HTTP_200_OK, tags=["Eventos"])
async def get_evento_data_from_id(eventoId: int, db: Session = Depends(db.get_database)):
    return crud.get_evento_data_from_id(db, eventoId)

"""

@app.post("/insertEvento", response_model=api_models.Evento, status_code=status.HTTP_200_OK, tags=["Eventos"])
async def insert_evento(evento: api_models.Evento, db: Session = Depends(db.get_database)):
    #evento.id = random.randint(0, 40000) # TODO cambiar
    if not (db_evento := crud.insert_evento(db, evento)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ese evento ya existe")
    return converters.apiEventoFromDBEvento(db_evento)

@app.put("/insertEventoImage", tags=["Eventos"], status_code=status.HTTP_200_OK)
async def insert_evento_image(image: UploadFile, _: str = Depends(get_verified_current_user)):
    with open(f'./eventoImages/{image.filename}', 'wb') as f:
        f.write(await image.read())

@app.post("/deleteEvento", response_model=api_models.Evento, status_code=status.HTTP_200_OK, tags=["Eventos"])
async def delete_evento(eventoId: str, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (evento := crud.get_evento(db, eventoId)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese evento no existe")

    deleted_evento = crud.delete_evento(db, evento)
    try:
        os.remove(f'./eventoImages/{deleted_evento.id}.png')
    except FileNotFoundError:
        pass
    return converters.apiEventoFromDBEvento(deleted_evento)


# ---------------------------  INTEGRANTE ------------------------------
@app.get("/getIntegrantes", response_model=list[api_models.Integrante], status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def get_integrantes(db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    return crud.get_integrantes(db)

@app.post("/insertIntegrante", response_model=api_models.Integrante, status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def insert_integrante(integrante: api_models.Integrante, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (db_integrante := crud.insert_integrante(db, integrante)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"'{integrante.username}' ya está en '{integrante.nombre}'")
    return db_integrante

@app.post("/deleteIntegrante", response_model=api_models.Integrante, status_code=status.HTTP_200_OK, tags=["Integrantes"])
async def delete_integrante(integrante: api_models.Integrante, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (integrante := crud.get_integrante(db, integrante)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese integrante no pertenece a esa cuadrilla")

    return crud.delete_integrante(db, integrante)


# ---------------------------  SEGUIDORES ------------------------------

@app.get("/getSeguidores", response_model=list[api_models.Seguidores], status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def get_seguidores(db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    seguidores = crud.get_seguidores(db)
    return [
        converters.apiSeguidorFromDBSeguidor(seguidor) 
        for seguidor in seguidores
    ]

@app.post("/insertSeguidores", response_model=api_models.Seguidores, status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def insert_seguidores(seguidores: api_models.Seguidores, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (db_seguidores := crud.insert_seguidores(db, seguidores)):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"'{seguidores.siguiendo}' ya sigue a '{seguidores.seguido}'")
    return converters.apiSeguidorFromDBSeguidor(db_seguidores) 


@app.post("/deleteSeguidor", response_model=api_models.Seguidores, status_code=status.HTTP_200_OK, tags=["Seguidores"])
async def delete_seguidor(seguidor: api_models.Seguidores, db: Session = Depends(db.get_database), _: str = Depends(get_verified_current_user)):
    if not (seguidor := crud.get_seguidor(db, seguidor)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ese usuario no sigue a ese otro usuario")

    deleted_seguidor = crud.delete_seguidor(db, seguidor)
    return converters.apiSeguidorFromDBSeguidor(deleted_seguidor) 


# ---------------------------  NOTIFICACIONES ------------------------------

@app.post('/notifications/subscribe', status_code=status.HTTP_202_ACCEPTED, tags=["Notifications"])
def suscribe_user_to_alert(token: FirebaseClientToken, username: str , e: str = Depends(get_verified_current_user)):
    print(f"username: {username}")
    print(f"currentUser: {e}")
    messaging.subscribe_to_topic([token.fcm_client_token], unidecode(username.replace(' ', '_')))
    messaging.subscribe_to_topic([token.fcm_client_token], 'All')


@app.post('/notifications/unsubscribe', status_code=status.HTTP_202_ACCEPTED, tags=["Notifications"])
def unsuscribe_user_to_alert(token: FirebaseClientToken, username: str , _: str = Depends(get_verified_current_user)):
    messaging.unsubscribe_from_topic([token.fcm_client_token], unidecode(username.replace(' ', '_')))
    messaging.unsubscribe_from_topic([token.fcm_client_token], 'All')


@app.post('/notifications/subscribeToUser', status_code=status.HTTP_202_ACCEPTED, tags=["Notifications"])
def suscribe_to_user(token: FirebaseClientToken, username: str , _: str = Depends(get_verified_current_user)):
    usernameNuevo= username+"2"
    messaging.subscribe_to_topic([token.fcm_client_token], unidecode(usernameNuevo.replace(' ', '_')))


@app.delete('/notifications/unsubscribeFromUser', status_code=status.HTTP_202_ACCEPTED, tags=["Notifications"])
def unsubscribe_from_user(token: FirebaseClientToken, username: str ,_: str = Depends(get_verified_current_user)):
    usernameNuevo= username+"2"
    topic_name = unidecode(usernameNuevo.replace(' ', '_'))
    print(topic_name)
    messaging.unsubscribe_from_topic([token.fcm_client_token], topic_name)



async def send_notification(message: Message, topic: str = 'All'):
    messaging.send(
        messaging.Message(
            data={k: f'{v}' for k, v in dict(message).items()},
            topic=unidecode(topic.replace(' ', '_'))
        )
    )

@app.post("/notifications", tags=["Notifications"])
async def send_broadcast_notification(message: Message, _: str = Depends(get_verified_current_user)):
    await send_notification(message)


@app.post("/notifications/{username}", tags=["Notifications"])
async def send_notification_to_user(username: str, message: Message, _: str = Depends(get_verified_current_user)):
    await send_notification(message, username)
