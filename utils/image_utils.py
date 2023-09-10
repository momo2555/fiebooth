from .file_utils import FileUtils
from typing import List
from errors.errors import WrongIamgePath, WrongImageId
import os
import re

class ImageUtils():
    
    @staticmethod
    def get_all_user_folders(user_name) -> List[str]:
        folders = FileUtils.get_all_photos_folder()
        user_folders = []
        for f in folders:
            f_name = ImageUtils.get_folder_name_from_path(f)
            f_user_name = f_name.split("_")[-1].replace("/") #security?
            if user_name == f_user_name:
                user_folders.append(f_name)
        return user_folders
    
    @staticmethod
    def get_folder_path_from_name(folder_name: str) -> str:
        photos_folder = FileUtils.get_photos_folder()
        folder_path = os.path.join(photos_folder, folder_name)
        return folder_path

    @staticmethod
    def get_folder_name_from_path(folder_path: str) -> str:
        folder_name = os.path.basename(os.path.normpath(folder_path))
        return folder_name
    
    # give the id of an image from its path 
    # (will be deleted after adding a database)
    @staticmethod
    def get_image_id_from_path(image_path: str) -> str:
        photos_folder = FileUtils.get_photos_folder()
        path_data = os.path.split(photos_folder)
        if len(path_data) > 1:
            image_name = path_data[1]
            folder_name = os.path.basename(path_data[0])
            return f"[{folder_name}]{image_name}"
        else:
            raise WrongIamgePath(f"The image path {image_path} has an incorrect format")
        
    # get the path from image id
    @staticmethod
    def get_image_path_from_id(image_id: str) -> str:
        match = re.match("\[(.+)\](.+\.png)", image_id)
        if image_id == match[0]:
            photos_folder = FileUtils.get_photos_folder()
            folder_name = match[1]
            image_name = match[2]
            return os.path.join(photos_folder, f"{folder_name}/{image_name}")
        else:
            raise WrongImageId()
        