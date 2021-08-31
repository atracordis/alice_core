from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    """
    Model for auth token
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Contains connected username token
    """
    username: Optional[str] = None


class User(BaseModel):
    """
    Mother class containing basic user data
    To be inherited by UserInDB
    """
    username: str


class UserInDB(User):
    """
    Contains hashed user password
    """
    hashed_password: str