from fastapi import HTTPException, Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from src.modules.auth.auth_handler import verify_token

security = HTTPBearer()


class RoleChecker:

    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):

        token = credentials.credentials

        payload = verify_token(token)

        if not payload:
            raise HTTPException(
                status_code=403,
                detail="Token inválido"
            )

        role = payload.get("role")

        if role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos"
            )

        return payload