import os
from datetime import datetime
from datetime import date
import time
from pathlib import Path
import tempfile
from glob import glob
from typing import List
import shutil
from pathlib import Path
import re
from errors.errors import FieboothFolderNotFound

class FileUtils:
    @staticmethod
    def get_home_dir():
        fiebooth_path = Path("/fiebooth")
        if fiebooth_path.exists():
            return fiebooth_path
        else:
            raise FieboothFolderNotFound("'/fiebooth' path not found; \
                                         please create the folder and give the access rights")

    @staticmethod
    def get_photos_folder() -> str:
        home_dir = FileUtils.get_home_dir()
        photos_path = os.path.join(home_dir, "photos")
        if not os.path.exists(photos_path):
            os.makedirs(photos_path, exist_ok=True)
        return photos_path
    
    @staticmethod
    def delete_photos_folder():
        photos_dir = FileUtils.get_photos_folder()
        if Path(photos_dir).exists():
            shutil.rmtree(photos_dir)

    @staticmethod
    def get_photo_thumbnails_folder() -> str:
        home_dir = FileUtils.get_home_dir()
        thumbnails_path = os.path.join(home_dir, "thumbnails")
        if not os.path.exists(thumbnails_path):
            os.makedirs(thumbnails_path, exist_ok=True)
        return thumbnails_path
    
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
    def get_logs_folder():
        # TO DO
        home_dir = FileUtils.get_home_dir()
        logs_dir = Path(home_dir, "logs")
        if not logs_dir.exists():
            logs_dir.mkdir()
        return logs_dir
    
    @staticmethod
    def get_new_session_log_file():
        logs_dir = FileUtils.get_logs_folder()
        day_date : datetime = datetime.fromtimestamp(time.time())
        logfile = day_date.strftime("logs_%d-%m-%y_%H-%M-%S.txt")
        return Path(logs_dir, logfile)
        

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
        config_path = os.path.join(home_dir, "config")
        if not os.path.exists(config_path):
            os.makedirs(config_path, exist_ok=True)
        return config_path
    
    @staticmethod
    def delete_image(image_path: str) -> None:
        if os.path.exists(image_path):
            os.remove(image_path)

    @staticmethod    
    def delete_folder(folder_name :str) -> None:
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name) 
    
    @staticmethod
    def get_all_users_names() -> List[str]:
        folders = FileUtils.get_all_photos_folder()
        users : List[str] = []
        for folder in folders:
            match = re.match("([0-9]{2}_){3}(.+)", os.path.basename(os.path.normpath(folder)))
            if match is not None:
                user_name = match[2]
                if not user_name in users:
                    users.append(user_name)
        return users
