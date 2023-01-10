from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str


class UserLoginIn(UserBase):
    password: str


class UserRegisterIn(UserBase):
    password: str
    role: str


class UserRegisterMaster(UserBase):
    password:str
