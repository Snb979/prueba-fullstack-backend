from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException

from src.modules.auth.auth_handler import verify_token


class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):

        credentials = await super().__call__(request)

        token = credentials.credentials

        data = verify_token(token)

        if data is None:
            raise HTTPException(
                status_code=403,
                detail="Token inválido"
            )

        return credentials