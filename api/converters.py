import api_models
import dbClasses

'''
Converts the db classes used by the ORM to objects to be send through the API.

Mapping 'api_models' with 'dbClasses'
'''

def apiEventoFromDBEvento(db_evento: dbClasses.Evento):
    return api_models.Evento(
        id = str(db_evento.id), # because db_evento.id is a UUID
        nombre = db_evento.nombre,
        fecha = db_evento.fecha.strftime('%d/%m/%Y'),
        descripcion = db_evento.descripcion,
        localizacion = db_evento.localizacion
    )

def apiCuadrillaAsistenteFromDBCuadrillaAsistente(cuadrilla_asistente: dbClasses.CuadrillaAsistente):
    return api_models.CuadrillaAsistente(
            nombre = cuadrilla_asistente.nombre,
            id = str(cuadrilla_asistente.id)
        )

def apiUsuarioAsistenteFormDBUsuarioAsistente(usuario_asistente: dbClasses.UsuarioAsistente):
    return api_models.UsuarioAsistente(
        username = usuario_asistente.username,
        idEvento = str(usuario_asistente.id)
    )

def apiUsuarioFromDBUsuario(db_usuario: dbClasses.Usuario):
    return api_models.Usuario(
        username=db_usuario.username, 
        email=db_usuario.email, 
        nombre=db_usuario.nombre, 
        fechaNacimiento=db_usuario.fechaNacimiento.strftime('%d/%m/%Y'),
        telefono=db_usuario.telefono
    )

def apiSeguidorFromDBSeguidor(db_seguidor: dbClasses.Seguidores):
    return api_models.Seguidores(
            seguidor = db_seguidor.siguiendo,
            seguido = db_seguidor.seguido
        )