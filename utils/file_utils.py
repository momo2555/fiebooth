import os
from datetime import datetime
from datetime import date
import time
from pathlib import Path
import tempfile
from glob import glob
from typing import List
import shutil

class FileUtils:
    @staticmethod
    def get_home_dir():
        return Path.home()
    
    @staticmethod
    def get_photos_folder() -> str:
        home_dir = FileUtils.get_home_dir()
        photos_path = os.path.join(home_dir, ".fiebooth/photos")
        if not os.path.exists(photos_path):
            os.makedirs(photos_path, exist_ok=True)
        return photos_path
    
    # Create the session folder and gives the name
    # If the folder exists it only gives the name
    @staticmethod
    def get_photos_sessions_dir(user_name : str) -> str:
        photos_dir = FileUtils.get_photos_folder()
        day_date : date = date.fromtimestamp(time.time())
        session_name : str= "{}_{}"
        session_name = session_name.format(day_date.strftime("%d_%m_%y"), user_name)
        session_path = os.path.join(photos_dir, session_name)
        if not os.path.exists (session_path):
            os.makedirs(session_path, exist_ok=True)
        return session_path
    
    @staticmethod
    def get_photo_file_name(user_name : str):
        session_dir : str = FileUtils.get_photos_sessions_dir(user_name)
        day_date : datetime = datetime.fromtimestamp(time.time())
        photo_name : str = "{}_{}.png"
        photo_name = photo_name.format(day_date.strftime("capture_%d%m%y_%H-%M-%S"), user_name)
        return os.path.join(session_dir, photo_name)
    

    @staticmethod
    def get_all_photos_folder() -> List[str]:
        photos_path = FileUtils.get_photos_folder()
        search_path = os.path.join(photos_path, "*/")
        folders = glob(search_path, recursive = False)
        return folders

    @staticmethod
    def create_logs_folder():
        if not os.path.exists("~/.fiebooth/logs"):
            os.mkdir("~/.fiebooth/logs")

    @staticmethod
    def get_temp_dir() -> str:
        temp_dir = os.path.join(tempfile.gettempdir(), "fiebooth")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    @staticmethod
    def get_all_photos_in_folder(folder_path: str) -> List[str]:
        search_path = os.path.join(folder_path, "*")
        photos = glob(search_path, recursive = False)
        return photos
    
    @staticmethod
    def get_config_folder() -> str:
        home_dir = FileUtils.get_home_dir()
        config_path = os.path.join(home_dir, ".fiebooth/config")
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        return config_path
    
    @staticmethod
    def delete_image(image_path: str) -> None:
        if os.path.exists(image_path):
            os.remove(image_path)
        
    def delete_folder(folder_name :str) -> None:
        if os.path.exists(folder_name):
                os.remove(folder_name)    