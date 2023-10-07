import pygame
from utils.file_utils import FileUtils
from controllers.cameraController import CameraController
from config import config
import logging
import time
from PIL import Image


class CameraUtils:
    
    @staticmethod
    def show_camera_stream_as_background(camera_controller: CameraController, window_context) -> None:
        array = camera_controller.get_frame_as_array()
        img = pygame.image.frombuffer(array.data, camera_controller.get_resolution(), 'RGB')
        window_context.blit(img, (0, 0))
        
    @staticmethod
    def save_picture(camera_controller: CameraController) -> str:
        img_name = FileUtils.get_photo_file_name(config["user_name"])
        t = time.time()
        camera_controller.capture_file(img_name)
        logging.getLogger("fiebooth").info(f"save time = {time.time() - t}")
        config["user_photos_len"] =  config["user_photos_len"] + 1
        config["total_photos_len"] =  config["total_photos_len"] + 1
        return img_name
        