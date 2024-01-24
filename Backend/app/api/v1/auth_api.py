import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Response, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.repository.user_repository import UserRepository
from app.dependency.repository import get_user_repository
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from app.util.logger import logger

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    logger.info("Creating Token ...")
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
            status_code=402,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # read user data
    user_data = user_repo.read_users_by_email(email=form_data.username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # take first element, because email_adresse should be unique
    user = user_data[0]

    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user["email_address"]}, expires_delta=access_token_expires
    )
    logger.info("Token created.")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    logger.info("Coockie setted.")
    return {"access_token": access_token, "token_type": "bearer", "success": True}


@router.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            logger.info("Token is invalid.")
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info("Token is valid.")
        return {"email": email}
    except JWTError:
        logger.info("Token is valid.")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/signup")
async def signup_user(
    signup_data: dict = Body(...),  # Using Body to accept a JSON object
    user_repo: UserRepository = Depends(get_user_repository),
):
    logger.info("Extracting User data..")
    firstname = signup_data.get("firstname")
    lastname = signup_data.get("lastname")
    email = signup_data.get("email")
    password = signup_data.get("password")
    officeLocation = signup_data.get("officeLocation")

    logger.info("Verifying if Email is already in use..")
    if user_repo.read_users_by_email(email):
        raise HTTPException(status_code=405, detail="Email already in use")
    logger.info("Email is valid..")

    user_data = {
        "firstname": firstname,
        "lastname": lastname,
        "email_address": email,
        "password": password,
        "officeLocation": officeLocation,
    }

    user_repo.create_user(user_data)
    logger.info("User inserted into database..")
    return {"message": "User created successfully"}
