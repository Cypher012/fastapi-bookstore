from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
# from app.auth import models
from .schemas import UserCreateModel, UserResponseModel, UserLogin, UserBooksModel
from .service import UserService
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,verify_password
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer,get_current_user, RoleChecker
from app.db.redis import add_jti_to_blocklist
from datetime import datetime

auth_router = APIRouter()
user_service =  UserService()
role_checker = RoleChecker(["admin", "user"])
REFRESH_TOKEN_EXPIRY = 7

@auth_router.post('/register', response_model=UserResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
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
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token({
        "email": user.email,
        "user_id": str(user.id),
        "role": user.role
    })

    refresh_token = create_access_token({
        "email": user.email,
        "user_id": str(user.id),
    }, refresh= True, expiry= timedelta(days=REFRESH_TOKEN_EXPIRY))
    
    return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "user": {
        "email": user.email,
        "user_id": str(user.id)
    }})

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data = token_details["user"])
        return JSONResponse(content={
            "access_token": new_access_token
        })
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired token")
       

@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _: bool = Depends(role_checker)):
    return user
        
@auth_router.get("/logout", status_code=status.HTTP_200_OK)
async def resolve_token(token_details = Depends(AccessTokenBearer())):
    jti = token_details["jti"]
    
    await add_jti_to_blocklist(jti)
    
    return {"message": "Logged out sucessfully"}
    

