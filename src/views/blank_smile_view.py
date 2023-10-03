from .stateView import StateView
from assets.assets import get_asset_uri
from controllers.cameraController import CameraController
from controllers.flashController import FlashController
from utils.camera_utils import CameraUtils
from utils.win_utils import CenterMode
from components.text_message import TextMessage
import time
import pygame

class BlankSmileView(StateView):
    def __init__(self, state_controller, window_context, camera):
        StateView.__init__(self, state_controller, window_context, "blank_smile", "ask_print")
        self.__camera : CameraController = camera
        self.__flash : FlashController = None
        self.__timer = 0
       

    def show(self):
        self.__flash = FlashController()
        self.__timer = time.time()
        self.__smile_text = TextMessage(self._window, "Smile :)",
                                            center_x=CenterMode.CENTER, font_size=400,
                                            center_y=CenterMode.CENTER, color=(67,134, 213))
        
    def setup(self):
        self._window.fill((255, 255, 255))
        self.__smile_text.setup()
        if time.time() - self.__timer > 0.3: 
            self._go_next_state()
        
    def destroy(self):
        self.__save_picture()
        self.__flash.clean()


    def __save_picture(self):
        self.__flash.flash_on()
        photo_name = CameraUtils.save_picture(self.__camera)
        self.__flash.flash_off()
        self._add_artifact("photo", photo_name)
        