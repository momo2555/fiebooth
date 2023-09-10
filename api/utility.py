from utils.file_utils import FileUtils
from utils.image_utils import ImageUtils
from api.models import SimpleUser

class ApiUtilities():
    def __init__(self):
        pass
    
    #return all folders name of a user
    def get_user_folder(self, user_name):
        return ImageUtils.get_all_user_folders(user_name)
    
    def get_image_path(self, image_id: str, user: SimpleUser) -> str:
        #user verfication
        return ImageUtils.get_image_path_from_id(image_id)
