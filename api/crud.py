from sqlalchemy.orm import Session
from dbClasses import User

def get_users(db: Session):
    return db.query(User).all()
