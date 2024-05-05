from datetime import timedelta, datetime
from os import environ

from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

import crud
import database as db

# ---------------------------------------------------------
#  Constants
# ---------------------------------------------------------
SECRET_KEY = environ['API_JWT_SECRET_KEY']
ALGORITHM = environ.get('API_JWT_ALGORITHM') or "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24  # One day

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


# ---------------------------------------------------------
#  Token Definitions
# ---------------------------------------------------------

class TokenResponse(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_in: int


class TokenData(BaseModel):
    username: str | None = None


class OAuth2RefreshTokenForm:
    def __init__(
            self,
            grant_type: str = Form(..., regex="refresh_token"),
            refresh_token: str = Form(...),
    ):
        self.grant_type = grant_type
        self.refresh_token = refresh_token


# ---------------------------------------------------------
#  OAUTH2
# ---------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/iniciarSesion")


# ---------------------------------------------------------
#  Utility Methods
# ---------------------------------------------------------

def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(data: dict) -> tuple[str, int]:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data, expires_delta=access_token_expires)
    return access_token, ACCESS_TOKEN_EXPIRE_MINUTES * 60


def create_refresh_token(data: dict):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_token(data, expires_delta=expires)


def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_verified_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(db.get_database)):
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise CREDENTIALS_EXCEPTION

        token_data = TokenData(username=username)

    except JWTError:
        raise CREDENTIALS_EXCEPTION

    if crud.get_user_password(db, username=token_data.username) is None:
        raise CREDENTIALS_EXCEPTION

    return token_data.username

# ---------------------------------------------------------
#  Data
# ---------------------------------------------------------

def apiDateStrToDatabaseStr(date: str) -> str:
    birthDateDay = date.split('/')[0]
    birthDateMonth = date.split('/')[1]
    birthDateYear = date.split('/')[2]
    return f'{birthDateYear}-{birthDateMonth}-{birthDateDay}'