import os
from config import config
from datetime import datetime
from datetime import date
import time


class FileUtils:
    @staticmethod
    def create_photos_folder() -> None:
        if not os.path.exists("~/.fiebooth/photos"):
            os.makedirs("~/.fiebooth/photos", exist_ok=True)
    
    # Create the session folder and gives the name
    # If the folder exists it only gives the name
    @staticmethod
    def get_photos_sessions_dir() -> str:
        FileUtils.create_photos_folder()
        day_date : date = date.fromtimestamp(time.time())
        session_name : str= "{}_{}"
        session_name = session_name.format(day_date.strftime("%d_%m_%y"), config.USER_NAME)
        session_path = os.path.join("~/.fiebooth/photos", session_name)
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

