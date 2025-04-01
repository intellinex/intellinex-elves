from typing import Annotated
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status

from src.core.config import settings

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.db.mongodb import get_async_db

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEMA = OAuth2PasswordBearer(tokenUrl="sign-in")

##
# Function for Create new JWT Token
# For user login or register
# #
def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


##
# Function for Decode JWT Token
# And make sure that token is not expired
# #
def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    

##
# Function for Verify Password fro User Input
# Use it when user login with Password
# #
def verify_password(plain_password, hashed_password):
    return PWD_CONTEXT.verify(plain_password, hashed_password)



##
# Function for Generate Hash Password
# For security ecrypt before store in database
# #
def get_hashed_password(password):
    return PWD_CONTEXT.hash(password)


##
# Helper Function for Get User Data
# #
async def get_user_collection (db: AsyncIOMotorDatabase = Depends(get_async_db)):
    return await db["users"]

# Fetch user data from database
async def get_user(username: str, collection: AsyncIOMotorCollection = Depends(get_user_collection)):
    return await collection.find_one({"username": username})


##
# Authentication Dependency
# Get user Data by Injection
# #
async def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEMA)]):
    """Get current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user_data = await get_user(username)
    if not user_data:
        raise credentials_exception
    return user_data


##
# Authenticate user function
# This use for user login
# #
async def authenticate_user(username: str, password: str):
    user_data = await get_user(username)
    if not user_data:
        return None
    if not verify_password(password, user_data["password"]):
        return None
    return user_data