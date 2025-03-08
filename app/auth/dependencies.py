from fastapi import HTTPException, Request,status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token

class AcessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(AcessTokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        if creds is None:
            print("No credentials provided")
            raise HTTPException(status_code=401, detail="Authorization token is missing")

        if creds.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        
        if not creds.credentials:
            raise HTTPException(status_code=403, detail="Invalid token credentials")
        
        token = creds.credentials

        token_data = decode_token(token)


        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")  
        
        
        if token_data["refresh"]:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type")

        return token_data
    
    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data is None:
            return False
        return True
