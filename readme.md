# FastUp Android App API REST and DB

## Using containers

### REST API with FastAPI

REST API implemented using FastAPI framework in Python and uvicorn to launch as a web server.

### PostgreSQL

Relational SQL database for persisting FestUp data.

### adminer

PostgreSQL UI for management.

## Others

Using `crontab` to delete previous events and their images:
- [crontab-job](./crontab-job): Archivo que define el comando de `crontab` (se ejecuta todos los días a las 10:10 UTC)
- [erase-events.sh](./erase-events.sh): Archivo bash que se ejecuta.
- [erase_events.py](./api/erase_events.py): Archivo python que se ejecuta dentro del contenedor.
