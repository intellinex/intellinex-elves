from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from src.model import jwt as JWT
from src.schema import user
from dotenv import load_dotenv
import os
import jwt
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from src.db.mongodb import db_instance

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="sign-in")

router = APIRouter()

# 🔹 Helper Functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)

async def get_user(username: str):
    """Retrieve user from MongoDB asynchronously."""
    return await db_instance.db["users"].find_one({"username": username})

async def authenticate_user(username: str, password: str):
    """Authenticate user by username and password."""
    user_data = await get_user(username)
    if not user_data:
        return None
    if not verify_password(password, user_data["password"]):  # Fix: Ensure key matches stored value
        return None
    return user_data

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🔹 Authentication Dependencies
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    except InvalidTokenError:
        raise credentials_exception

    user_data = await get_user(username)
    if not user_data:
        raise credentials_exception
    return user_data

async def get_current_active_user(
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """Check if the current user is active."""
    if current_user.get("disabled", False):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user



# 🔹 User Authentication (Login)
@router.post("/sign-in", response_model=JWT.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """Login user and return JWT token."""

    user = await authenticate_user(form_data.username, form_data.password)  # Fix: Await the function
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)

    await db_instance.db["users"].update_one(
        {"username": user["username"]},
        {"$set": {"last_login": datetime.now(timezone.utc)}}
    )
    
    return JWT.Token(access_token=access_token, token_type="bearer")




# 🔹 User Registration (Sign-Up)
@router.post("/register", response_model=JWT.Token)
async def register_user(
    username: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    password: str = Form(...),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
):
    """Register a new user using form-data."""
    if await db_instance.db["users"].find_one({"username": username}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    if await db_instance.db["users"].find_one({"email": email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    hashed_password = get_hashed_password(password)
    
    new_user = {
        "username": username,
        "email": email,
        "phone": phone,
        "password": hashed_password,
        "first_name": first_name,
        "last_name": last_name,
        "role": "candidate",
        "last_login": datetime.now(timezone.utc),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    await db_instance.db["users"].insert_one(new_user)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)

    return JWT.Token(access_token=access_token, token_type="bearer")



# 🔹 Retrieve Logged-in User
@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[user.User, Depends(get_current_active_user)]
):
    """Retrieve current user information."""
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user.get("email"),
        "first_name": current_user.get("first_name"),
        "last_name": current_user.get("last_name"),
        "disabled": current_user.get("disabled", False),
    }