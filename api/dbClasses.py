from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'usuario'
    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String)
    nombre = Column(String)