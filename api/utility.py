from utils.file_utils import FileUtils
from utils.image_uils import ImageUtils

class ApiUtilities():
    def __init__(self):
        pass
    
    #return all folders name of a user
    def get_user_folder(self, user_name):
        return ImageUtils.get_all_user_folders(user_name)
