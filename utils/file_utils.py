import os
from config import config
from datetime import datetime
from datetime import date
import time
from pathlib import Path
import tempfile


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
    def get_photos_sessions_dir() -> str:
        photos_dir = FileUtils.get_photos_folder()
        day_date : date = date.fromtimestamp(time.time())
        session_name : str= "{}_{}"
        session_name = session_name.format(day_date.strftime("%d_%m_%y"), config.USER_NAME)
        session_path = os.path.join(photos_dir, session_name)
        if not os.path.exists (session_path):
            os.makedirs(session_path, exist_ok=True)
        return session_path
    
    @staticmethod
    def get_photo_file_name():
        session_dir : str = FileUtils.get_photos_sessions_dir()
        day_date : datetime = datetime.fromtimestamp(time.time())
        photo_name : str = "{}_{}.png"
        photo_name = photo_name.format(day_date.strftime("capture_%d%m%y_%H-%M-%S"), config.USER_NAME)
        return os.path.join(session_dir, photo_name)
    

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