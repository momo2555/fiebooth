from pydantic import BaseModel
from typing import Union, Any

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

class SimpleUser(BaseModel):
    username: str
    password: str
    hashpassword: str

class ConfigDescriptor(BaseModel):
    key: str
    value: Any