from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str


class RegisterSchema(BaseModel):
    username: str
    password: str

