from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud
import database as db

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/getUsers")
def getUsers(db: Session = Depends(db.get_database)):
    users = crud.get_users(db)
    user_json = []
    for user in users:
        user_json.append({"username": user.username, "password": user.password, "email": user.email, "nombre": user.nombre})
    return user_json