from .stateView import StateView
from views.stateView import StateView
from controllers.cameraController import CameraController
from controllers.buttonsController import ButtonsController
from utils.camera_utils import CameraUtils
from utils.image_utils import ImageUtils
import pygame
from pygame_widgets.slider import Slider
import pygame_widgets
from components.simple_slider import SimpleSlider
from config import config
import random as rd
import time

class DiaporamaView(StateView):
    def __init__(self, state_controller, window_context, camera):
        StateView.__init__(self, state_controller, window_context, "diaporama", "countdown")
        self.__camera : CameraController = camera
        self.__buttons_controller : ButtonsController = ButtonsController()
        self.__contr_slider : SimpleSlider = None
        self.__photos = []
        self.__current_photo : str = None
        self.__timer : float = None 
        
        

    def __init_buttons_events(self):
        self.__buttons_controller.add_button(pygame.K_a, self.__trigger_shot_callback)
        self.__buttons_controller.add_button(pygame.K_UP, self.__config_contrast_up)
        self.__buttons_controller.add_button(pygame.K_DOWN, self.__config_contrast_down)

    def __trigger_shot_callback(self):
        self._go_next_state()

    def __config_contrast_up(self):
        self.__contr_slider.set_value(self.__contr_slider.get_value() + 1)
        
    def __config_contrast_down(self):
        self.__contr_slider.set_value(self.__contr_slider.get_value() - 1)

    def __config_lum_up(self):
        pass

    def __config_lum_down(self):
        pass
 
    
    def __choose_photo(self):
        length = len(self.__photos)
        self.__current_photo = self.__photos[rd.randint(0, length -1)]
        self.__timer = time.time()

    def show(self):
        self.__init_buttons_events()
        self.__photos = ImageUtils.get_all_user_photos_path(config.USER_NAME)
        self.__choose_photo()

    def __draw_photo(self):
        self.__img = pygame.image.load(self.__current_photo).convert()
        self._window.blit(self.__img, (0, 0))

    def setup(self):
        if time.time() - self.__timer > 4:
            self.__choose_photo()
        self.__draw_photo()
        self.__buttons_controller.setup()
    
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()
         

    