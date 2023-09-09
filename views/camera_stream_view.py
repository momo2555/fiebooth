from views.stateView import StateView
from controllers.cameraController import CameraController
from controllers.buttonsController import ButtonsController
from utils.camera_utils import CameraUtils
import pygame

class CameraStreamView(StateView):
    def __init__(self, state_controller, window_context, camera):
        StateView.__init__(self, state_controller, window_context, "camera_stream", "countdown")
        self.__camera : CameraController = camera
        self.__buttons_controller : ButtonsController = ButtonsController()
        

    def __init_buttons_events(self):
        self.__buttons_controller.add_button(pygame.K_a, self.__trigger_shot_callback)

    def __trigger_shot_callback(self):
        self._go_next_state()

    def __config_contrast_up(self):
        pass

    def __config_contrast_down(self):
        pass

    def __config_lum_up(self):
        pass

    def __config_lum_down(self):
        pass
 
    def show(self):
        self.__init_buttons_events()

    def setup(self):
        CameraUtils.show_camera_stream_as_background(self.__camera, self._window)
        self.__buttons_controller.setup()

    def destroy(self):
        self.__buttons_controller.clear_triggers()



