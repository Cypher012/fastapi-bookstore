from fastapi import HTTPException, Request,status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from app.db.redis import token_in_block_list


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        if creds is None:
            print("No credentials provided")
            raise HTTPException(status_code=401, detail="Authorization token is missing")

        if creds.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        
        if not creds.credentials:
            raise HTTPException(status_code=403, detail="Invalid or expired token credentials")
        
        token = creds.credentials

        token_data = decode_token(token)

        if await token_in_block_list(token_data['jti']):
            raise HTTPException(status_code=403, detail="Invalid or expired token credentials")

        self.verify_token_data(token_data)

        return token_data
    
    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Please Overide this method in child classes")

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data is None:
            return False
        return True


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")
    

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token")