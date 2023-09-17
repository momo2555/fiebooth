import yaml
from yaml import Loader, Dumper
from utils.file_utils import FileUtils
import os
import shutil
from collections.abc import MutableMapping
from typing import Any, Iterator, List, Dict
import logging

class Config(MutableMapping):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.instance.__init_config()
            cls.instance.logger = logging.getLogger("fiebooth")
            cls.instance.logger.info("INIT CONFIG -------------------------------------------------------------")
        return cls.instance
    
    def __read_config(cls, config_path):
        with open(config_path, "r") as f:
            cls.__config : Dict[str, Any] = yaml.load(f, Loader=Loader)
        
    def __write_config(cls):
        with open(cls.__config_file, "w") as f:
            yaml.dump(cls.__config,  f, Dumper=Dumper)

    def __create_new_config(cls, config_path):
        cls.logger.info("Create new config")
        shutil.copyfile("config/config.yaml", config_path)

    def __init_config(cls):
        config_folder = FileUtils.get_config_folder()
        config_file = os.path.join(config_folder, "config.yaml")
        if not os.path.exists(config_file):
            cls.__create_new_config(config_file)
        cls.__read_config(config_file)
        cls.__config_file = config_file
    
    def __getitem__(cls, __key: Any) -> Any:
        
        
        return cls.__config[__key]
    
    def __getattribute__(cls, __name: str) -> Any:
        try:
            config = super().__getattribute__('_Config__config')
            
            if __name in config.keys():
                
                return config[__name]
            else:
                return super().__getattribute__(__name)
        except:
            return super().__getattribute__(__name)
    
    
    def __setitem__(cls, __key: Any, __value: Any) -> None:
        
        cls.__config[__key]  = __value
        
        cls.logger.info(f"change config {__key}, {__value}")
        cls.__write_config()
    
    def __len__(cls) -> int:
        cls = cls.instance
        return len(cls.__config)
    
    def __delitem__(self, __key: Any) -> None:
        raise Exception("Delete a config is forbiden !")
    
    def __iter__(cls) -> Iterator:
        cls = cls.instance
        return iter(cls.__config)
    
    
