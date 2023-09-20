from pydantic import BaseModel
from typing import Union, Any
from enum import Enum
from typing import Any, Dict

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

class ExchangeType(Enum):
    REQUEST = 0
    RESPONSE = 1

class ExchangeRequest(Enum):
    EDIT_CONFIG_REQUEST = 0
    GET_CONFIG_REQUEST = 1

class ExchangeResponse(Enum):
    EDIT_SUCCESS = 0
    GET_SUCCESS = 1
    CONFIG_NOT_FOUND = 2

class DataExchange(BaseModel):
    type: str
    value: str
    args: Dict[str, Any] = {}
