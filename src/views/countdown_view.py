from .stateView import StateView
from assets.assets import get_asset_uri
from controllers.cameraController import CameraController
from utils.camera_utils import CameraUtils
from utils.win_utils import CenterMode
from components.text_message import TextMessage
from components.fiebooth_logo import FieboothLogo, LogoColorMode
import time
import pygame


class CountDownView(StateView):
    def __init__(self, state_controller, window_context, camera):
        StateView.__init__(self, state_controller, window_context, "countdown", "blank_smile")
        self.__timer = 0
        self.__camera :CameraController = camera
        self.__font = get_asset_uri("BradBunR.ttf")

    def show(self):
        self.__timer = time.time()
        self.__logo = FieboothLogo(self._window, LogoColorMode.LIGHT)

    def setup(self):
        self.__show_camera_stream()
        diff_time = time.time() - self.__timer
        if diff_time > 0 and diff_time <= 1:
            self.__show_count("3")
        elif diff_time > 1 and diff_time <= 2:
            self.__show_count("2")
        elif diff_time > 2 and diff_time <= 3:
            self.__show_count("1")
        else:
            self._go_next_state()
        
    def __show_camera_stream(self):
        CameraUtils.show_camera_stream_as_background(self.__camera, self._window)

    def __show_count(self, number):
        count = TextMessage(self._window, number,
                                            center_x=CenterMode.CENTER, font_size=400,
                                            center_y=CenterMode.CENTER, color=(67,134, 213))
        count.setup()
        self.__logo.setup()