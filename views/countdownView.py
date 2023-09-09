from .stateView import StateView
from assets.assets import get_asset_uri
from controllers.cameraController import CameraController
from utils.camera_utils import CameraUtils
import time
import pygame

class CountDownView(StateView):
    def __init__(self, state_controller, window_context, buttons_controller, camera):
        StateView.__init__(self, state_controller, window_context, buttons_controller, "countdown", "ask_print")
        self.__timer = 0
        self.__camera :CameraController = camera
        self.__font = get_asset_uri("BradBunR.ttf")

    def show(self):
        print("show countdown")
        self.__timer = time.time()
        print("timer countdoan set")
        self.__camera.start()
        print("camera started")

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
            self.__save_picture()
            self._go_next_state()
        

    def destroy(self):
        self.__camera.stop()

    def __show_camera_stream(self):
        CameraUtils.show_camera_stream_as_background(self.__camera, self._window)

    def __show_count(self, number):
        font_obj = pygame.font.Font(self.__font, 100)
        text_obj = font_obj.render(number, True, (229, 40, 34))
        self._window.blit(text_obj, (150, 150))
    
    def __save_picture(self):
        print(CameraUtils.save_picture(self.__camera))
        pass