import yaml
from yaml import Loader, Dumper
from utils.file_utils import FileUtils
import os
import shutil
from collections.abc import MutableMapping
from typing import Any, Iterator, List, Dict
from dotenv import load_dotenv, set_key, find_dotenv, dotenv_values
import hashlib
import time
import random as rd
from pathlib import Path

class Env(MutableMapping):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Env, cls).__new__(cls)
            cls.instance.__init_env()
        return cls.instance
    
    def __read_env(cls):
        cls.__env = dotenv_values(".env")
        

    def __create_new_env(cls):
        f = open(".env", "wt")
        f.write("#ENV FIEBOOTH FILE")
        f.close()
        key = hashlib.sha256(f"{time.time() * rd.randint(1, 10000000000)}".encode()).hexdigest()
        set_key(find_dotenv(), "ALGORITHM", "HS256")
        set_key(find_dotenv(), "SECRET_KEY", key)
        set_key(find_dotenv(), "ADMIN_PASSWORD", "adminpassword")
        set_key(find_dotenv(), "ACCESS_TOKEN_EXPIRE_MINUTES", "120")
        set_key(find_dotenv(), "LOAD_MESSAGE", "Hi fiebooth !")

    def __init_env(cls):
        env_file = ".env"
        if not Path(env_file).exists():
            cls.__create_new_env()
        cls.__read_env()
    
    def __getitem__(cls, __key: Any) -> Any:
        return cls.__env[__key]
    
    def __getattribute__(cls, __name: str) -> Any:
        try:
            env = super().__getattribute__('_Env__env')
            
            if __name in env.keys():
                
                return env[__name]
            else:
                return super().__getattribute__(__name)
        except:
            return super().__getattribute__(__name)
    
    def __setitem__(cls, __key: Any, __value: Any) -> None:
        raise Exception("ENV config are readOnly !")
    
    def __len__(cls) -> int:
        cls = cls.instance
        return len(cls.__env)
    
    def __delitem__(self, __key: Any) -> None:
        raise Exception("Delete a config is forbiden !")
    
    def __iter__(cls) -> Iterator:
        cls = cls.instance
        return iter(cls.__env)
    
    
