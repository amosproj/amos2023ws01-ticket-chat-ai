import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.repository.user_repository import UserRepository
from app.dependency.repository import get_user_repository
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=15
        )  # Standardablaufzeit: 15 Minuten
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_repo: UserRepository = Depends(get_user_repository),
):
    # check userdata
    is_authenticated = user_repo.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not is_authenticated:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # read user data
    user_data = user_repo.read_users_by_email(email=form_data.username)
    if not user_data:
        raise HTTPException(status_code=400, detail="User not found")

    # take first element, because email_adresse should be unique
    user = user_data[0]

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user["email_address"]}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}
