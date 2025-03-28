from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from app.config import Config
import uuid
import logging

passwd_context = CryptContext(
    schemes= ['bcrypt'],
)

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {}
    payload["user"] = user_data
    if expiry:
        expire = datetime.now() + expiry
    else:
        expire = datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    
    payload["exp"] = expire 
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh
    
    token = jwt.encode(
        payload = payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
        jwt=token,
        key=Config.JWT_SECRET,
        algorithms=Config.JWT_ALGORITHM
    )
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Please log in again.")
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None