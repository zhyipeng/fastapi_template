from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str


class RegisterSchema(BaseModel):
    username: str
    password: str

