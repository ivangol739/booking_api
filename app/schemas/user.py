from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str