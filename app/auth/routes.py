from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
# from app.auth import models
from .schemas import UserCreateModel, UserResponseModel, UserLogin
from .service import UserService
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,verify_password
from fastapi.responses import JSONResponse


auth_router = APIRouter()
user_service =  UserService()

REFRESH_TOKEN_EXPIRY = 7

@auth_router.post('/register', response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def  create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exist = await user_service.user_exists(email, session)

    if user_exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login', response_model=UserResponseModel)
async def login_user(login_date: UserLogin, session: AsyncSession = Depends(get_session)):
    email = login_date.email 
    password = login_date.password

    user = await user_service.get_user_by_email(email, session)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({
        "email": user.email,
        "user_id": str(user.id),
    })

    refresh_token = create_access_token({
        "email": user.email,
        "user_id": str(user.id),
    }, refresh= True, expiry= timedelta(days=REFRESH_TOKEN_EXPIRY))
    
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "user": {
        "email": user.email,
        "user_id": str(user.id)
    }})
