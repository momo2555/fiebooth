from views.stateView import StateView
from controllers.cameraController import CameraController
from controllers.buttonsController import ButtonsController
from utils.camera_utils import CameraUtils
import pygame

class CameraStreamView(StateView):
    def __init__(self, state_controller, window_context, buttons_controller, camera):
        StateView.__init__(self, state_controller, window_context,buttons_controller, "camera_stream", "countdown")
        self.__camera : CameraController = camera
        self.__buttons_controller : ButtonsController= buttons_controller
        self.__init_buttons_event()

    def __init_buttons_event(self):
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
        self.__camera.start()
        pass

    def setup(self):
        CameraUtils.show_camera_stream_as_background(self.__camera, self._window)

    def destroy(self):
        print("destroy camera from camera stream")
        self.__camera.stop()
        print("end of destroy")



