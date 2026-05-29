from pydantic import BaseModel


class UserLoginResponse(BaseModel):

    id: int
    username: str
    email: str
    role: str


class LoginResponse(BaseModel):

    access_token: str
    token_type: str
    user: UserLoginResponse