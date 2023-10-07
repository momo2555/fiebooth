from utils.file_utils import FileUtils
from utils.image_utils import ImageUtils
from api.models import SimpleUser
from typing import List
from .models import SimpleUser, ConfigDescriptor
from threading import Lock

class ApiUtilities():
    def __init__(self, connection):
        self.__lock = Lock()
        self.__conn = connection
    
    #return all folders name of a user
    def get_user_folder(self, user_name):
        return ImageUtils.get_all_user_folders(user_name)
    
    def get_image_path(self, image_id: str, user: SimpleUser) -> str:
        #user verfication
        return ImageUtils.get_image_path_from_id(image_id)
    
    def get_image_thumbnail_path(self, image_id: str, user: SimpleUser) -> str:
        return ImageUtils.get_image_thumbnail_by_id(image_id)
    
    def delete_image(self, image_id: str):
        image_path = ImageUtils.get_image_path_from_id(image_id)
        FileUtils.delete_image(image_path)
    
    def delete_all_user_images(self, user_name : str):
        photos_id = self.get_all_user_photos(user_name)
        map(self.delete_image, photos_id)
    
    def delete_folder(self, folder_name : str):
        folder_path = ImageUtils.get_folder_path_from_name(folder_name)
        FileUtils.delete_folder(folder_path)

    def delete_all_images(semf):
        FileUtils.delete_photos_folder()
    
    def get_photos_in_folder(self, folder_name: str) -> List[str]:
        folder_path = ImageUtils.get_folder_path_from_name(folder_name)
        photos_path = FileUtils.get_all_photos_in_folder(folder_path)
        photos_id = list(map(ImageUtils.get_image_id_from_path, photos_path))
        return photos_id
    
    def get_all_user_photos(self, user_name: str) -> List[str]:
        photos_path = ImageUtils.get_all_user_photos_path(user_name)
        photos_id = list(map(ImageUtils.get_image_id_from_path, photos_path))
        return photos_id

    def get_all_photos(self):
        return ImageUtils.get_all_images()
    
    def get_all_users(self):
        return FileUtils.get_all_users_names()

    def create_new_user(self, new_user: SimpleUser):
        with self.__lock:
            self.__conn.send({
                "type" : "request",
                "value" : "createUser",
                "userName" : new_user.username,
                "userPassword" : new_user.hashpassword,
            })
            response = self.__conn.recv()
            if response["type"] == "response":
                if response["value"] == "userCreated":
                    return {
                        "user" : "created",
                    }
    def get_config(self, param: str):
        with self.__lock:
            self.__conn.send({
                "type" : "request",
                "value" : "getConfig",
                "configKey" : param
            })
            response = self.__conn.recv()
            if response["type"] == "response":
                if response["value"] == "getSuccess":
                    return {
                        "key" : param,
                        "value" : response["configValue"]
                    }
                
    def set_config(self, conf: ConfigDescriptor):
        with self.__lock:
            self.__conn.send({
                "type" : "request",
                "value" : "setConfig",
                "configKey" : conf.key,
                "configValue" : conf.value
            })
            response = self.__conn.recv()
            if response["type"] == "response":
                if response["value"] == "setSuccess":
                    old_value = conf.value
                    return {
                        "key" : response["configKey"],
                        "value" : response["configValue"]
                    }
                
    def print_photo(self, image_id: str):
        with self.__lock:
            self.__conn.send({
                "type" : "request",
                "value" : "print",
                "imageId" : image_id
            })
            response = self.__conn.recv()
            if response["type"] == "response":
                if response["value"] == "getSuccess":
                    return {
                        "print" : "sent",
                    }

