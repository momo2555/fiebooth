from picamera2 import Picamera2
from utils.win_utils import WinUtils
import logging

class CameraController:
    def __init__(self):
        width, height = WinUtils.get_screen_size()
        self.logger = logging.getLogger("fiebooth")
        self.__res = (width, height)
        self.logger.info(f"Résolution de l'écran {self.__res}")
        self.__camera = Picamera2()
        self.__camera.preview_configuration.main.size = self.__res
        self.__camera.preview_configuration.main.format = 'BGR888'
        self.__camera.configure("preview")
        self.__camera.set_controls({"AfMode":2, "AfTrigger" : 0})
        pass
    
    def start(self):
        self.__camera.start()

    def stop(self):
        self.__camera.stop()

    def get_resolution(self):
        return self.__res
    
    def get_frame_as_array(self):
        return self.__camera.capture_array()
