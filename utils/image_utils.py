from .file_utils import FileUtils
from typing import List
from errors.errors import WrongIamgePath, WrongImageId
import os
import time
import pygame
from config import config
import re
import logging
from PIL import Image, ImageOps, ImageEnhance

class ImageUtils():
    @staticmethod
    def logger():
         return logging.getLogger("fiebooth")

    @staticmethod
    def get_all_user_folders(user_name) -> List[str]:
        folders = FileUtils.get_all_photos_folder()
        user_folders = []
        for f in folders:
            f_name = ImageUtils.get_folder_name_from_path(f)
            f_user_name = f_name.split("_")[-1].replace("/", "") #security?
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
    
    @staticmethod
    def create_temp_resized_image(image_path: str) -> str:
        #create temp directory
        tmp_dir = FileUtils.get_temp_dir()
        tmp_img = os.path.join(tmp_dir, f"fb_{int(time.time())}.png")
        resize_img = pygame.transform.scale(pygame.image.load(image_path),(config.width_printer, config.height_printer))
        pygame.image.save(resize_img, tmp_img)
        ImageUtils.logger().info(f"temp file {tmp_img} saved after rescaling image")
        return tmp_img

    @staticmethod
    def get_all_user_photos_path(user_name) -> List[str]:
        folders : List[str] = list(map(ImageUtils.get_folder_path_from_name, 
                           ImageUtils.get_all_user_folders(user_name)))
        photos = []
        for f in folders:
            photos.extend(FileUtils.get_all_photos_in_folder(f))
        return photos

    @staticmethod  
    def image_transform(image_path, contrast : float = None, brightness : float = None, scale = None):
        im = Image.open(image_path)
        #rescale
        if scale is not None:
            im = im.resize(scale)
        im_gray = ImageOps.grayscale(im)
        #contrast
        if contrast is None : contrast = 1
        cont_enhancer = ImageEnhance.Contrast(im_gray)
        im_cont = cont_enhancer.enhance(contrast)
        #brightness
        if brightness is None : brightness = 1
        bright_enhaancer = ImageEnhance.Brightness(im_cont)
        im_final = bright_enhaancer.enhance(brightness)
        return im_final
    
    @staticmethod
    def image_transform_pyg(image_path, contrast : float = None, brightness : float = None, scale = None):
        im = ImageUtils.image_transform(image_path, contrast, brightness, scale)
        #return a pygame image object
        im = im.convert('RGB')
        mode = im.mode
        size = im.size
        data = im.tobytes()
        image_tf = pygame.image.fromstring(data, size, mode)
        #return transformed image
        return image_tf
    
        


        