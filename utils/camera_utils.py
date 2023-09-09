import pygame
from utils.file_utils import FileUtils
from controllers.cameraController import CameraController
class CameraUtils:
    @staticmethod
    def show_camera_stream_as_background(camera_controller: CameraController, window_context) -> None:
        array = camera_controller.get_frame_as_array()
        img = pygame.image.frombuffer(array.data, camera_controller.get_resolution(), 'RGB')
        window_context.blit(img, (0, 0))
        

    @staticmethod
    def save_picture(camera_controller: CameraController) -> str:
        array = camera_controller.get_frame_as_array()
        img = pygame.image.frombuffer(array.data, camera_controller.get_resolution(), 'RGB')
        img_name = FileUtils.get_photo_file_name()
        pygame.image.save(img, img_name)
        return img_name
        