from picamera2 import Picamera2, Preview
from utils.win_utils import WinUtils
from PIL import Image
import threading
import logging
import time
import cv2

class CameraController:
    def __init__(self):
        width, height = WinUtils.get_screen_size()
        self.logger = logging.getLogger("fiebooth")
        self.__res = (width, height)
        self.logger.info(f"Résolution de l'écran {self.__res}")
        self.__camera = Picamera2()

        self.__preview_config = self.__camera.create_preview_configuration(main={
            "size" : self.__res,
            "format" : 'BGR888',
        }
        )
        self.__still_config = self.__camera.create_still_configuration(main={
            "size" : (4624, 3472),
            "format" : 'BGR888',
        },
        buffer_count=1
        )
        #self.__camera.preview_configuration.main.size = self.__res
        #self.__camera.preview_configuration.main.format = 'BGR888'
        #self.__camera.configure("preview")
        self.__camera.configure(self.__preview_config)
        self.__camera.set_controls({"AfMode":2, "AfTrigger" : 0})
    
    def start(self):
        self.__camera.start()

    def stop(self):
        self.__camera.stop()

    def get_resolution(self):
        return self.__res
    
    def get_frame_as_array(self):
        return self.__camera.capture_array()
    
    def capture(self) -> Image:
        return self.__camera.capture_image()
    
    def capture_file(self, image_name) -> Image:
        self.stop()

        #self.__camera.preview_configuration.main.size = (4000, 3000)
        #self.__camera.configure("preview")
        self.__camera.configure(self.__still_config)
        self.start()
        array_capture = self.__camera.capture_array()
        save_task = threading.Thread(target=self.__save_image, args=(array_capture, image_name))
        save_task.start()
        #self.__camera.capture_file(image_name)
        self.stop()
        #self.__camera.preview_configuration.main.size = self.__res
        #self.__camera.configure("preview")
        self.__camera.configure(self.__preview_config)
        self.start()

        #return a small image
        return array_capture

    def __save_image(self, array_capture, image_name):
        beg = time.time()
        cv2.imwrite(image_name, array_capture)
        self.logger.info(f"Image saved ! => Time in thread = {time.time() - beg}s")
