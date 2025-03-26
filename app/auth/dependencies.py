from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from abc import ABC, abstractmethod
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main import get_session
from .utils import decode_token
from app.db.redis import token_in_block_list
from .service import UserService
from dataclasses import dataclass
from typing import List
from .models import User

user_service = UserService()

class TokenBearer(HTTPBearer, ABC):
    def __init__(self, auto_error: bool = False):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        if not creds or creds.scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication scheme")

        token_data = self.validate_token(creds.credentials)
        await self.check_revocation(token_data["jti"])
        self.verify_token_data(token_data)

        return token_data

    def validate_token(self, token: str) -> dict:
        """Decodes and validates JWT token."""
        token_data = decode_token(token)
        if not token_data:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
        return token_data

    async def check_revocation(self, jti: str) -> None:
        """Checks if token is revoked in Redis."""
        if await token_in_block_list(jti):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Token has been revoked. Please get a new one.")

    @abstractmethod
    def verify_token_data(self, token_data: dict) -> None:
        """Ensures subclass implements custom token checks."""
        pass


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh"):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Access token required, not a refresh token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh"):
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Refresh token required, not an access token")

async def get_current_user(token_details=Depends(AccessTokenBearer()), session: AsyncSession=Depends(get_session)):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user
    

class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles
        
    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource")
        return current_user
      