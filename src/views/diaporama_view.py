from .stateView import StateView
from views.stateView import StateView
from controllers.cameraController import CameraController
from controllers.buttons_controller import ButtonsController
from controllers.transform_controller import TransformController
from utils.camera_utils import CameraUtils
from utils.image_utils import ImageUtils
from utils.win_utils import WinUtils, CenterMode
import pygame
from components.simple_slider import SimpleSlider
from components.text_message import TextMessage
from config import config
import random as rd
import time
from assets.assets import get_asset_uri
import os
from utils.colors_utils import FiColor

class DiaporamaView(StateView):
    def __init__(self, state_controller, window_context, camera):
        StateView.__init__(self, state_controller, window_context, "diaporama", "countdown")
        self.__camera : CameraController = camera
        self.__buttons_controller : ButtonsController = ButtonsController()
        self.__photos = []
        self.__current_photo : str = None
        self.__timer : float = None 
        self.__diaporama_text : TextMessage = None
        self.__transform : TransformController = None

    def __init_buttons_events(self):
        self.__buttons_controller = ButtonsController()
        self.__buttons_controller.add_button(config.green_btn, self.__trigger_shot_callback, key=pygame.K_a)
        self.__buttons_controller.add_button(1, self.__config_contrast_up, key=pygame.K_UP)
        self.__buttons_controller.add_button(2, self.__config_contrast_down, key=pygame.K_DOWN)
        self.__buttons_controller.add_button(3, self.__config_brightness_up, key=pygame.K_RIGHT)
        self.__buttons_controller.add_button(4, self.__config_brightness_down, key=pygame.K_LEFT)

    def __trigger_shot_callback(self, e):
        self._go_next_state()

    def __config_contrast_up(self, e):
        self.__transform.contrast_up()
        
    def __config_contrast_down(self, e):
        self.__transform.contrast_down()

    def __config_brightness_up(self, e):
        self.__transform.brightness_up()

    def __config_brightness_down(self, e):
        self.__transform.brightness_down()
        pass
 
    
    def __choose_photo(self):
        self.__photos = ImageUtils.get_all_user_photos_path(config.user_name)
        length = len(self.__photos)
        if length > 0:
            self.__current_photo = self.__photos[rd.randint(0, length -1)]
        else:
            self.__current_photo = get_asset_uri("accueil.jpg")
        self.__timer = time.time()

    def show(self):
        self.__init_buttons_events()
        self.__choose_photo()
        self.__transform = TransformController(self._window, self.__current_photo)
        self.__diaporama_text = TextMessage(self._window, "Diaporama", color=FiColor.HIGHLIGHT,
                                            x = WinUtils.wprct(0.1),
                                            y = WinUtils.hprct(0.1),
                                            center_y=CenterMode.BOTTOM, font_size=WinUtils.hprct(0.06))
        self.__images_counter_text = TextMessage(self._window, f"{config.user_photos_len}", color=FiColor.WHITE,
                                            x = WinUtils.wprct(0.07),
                                            y = WinUtils.hprct(0.053),
                                            center_y=CenterMode.TOP, font_size=WinUtils.hprct(0.06))

    def __draw_photo(self):
        try:
            if os.path.exists(self.__current_photo):
                self.__img = pygame.image.load(self.__current_photo).convert()
            else:
                self.__choose_photo()
        except pygame.error as e:
            self._logger.warning(f"Image format not supported : {self.__current_photo}")
            
        (sw, sh) = (WinUtils.wprct(0.5), WinUtils.hprct(0.5))
        pos = (WinUtils.wprct(0.45), WinUtils.hprct(0.25))
        self.__img = pygame.transform.scale(self.__img, (sw, sh))
        self._window.blit(self.__img, pos)
    
    def __draw_photos_length(self):
        (w, h) = (WinUtils.wprct(0.13), WinUtils.hprct(0.08))
        (x, y) = (WinUtils.wprct(0.05), WinUtils.hprct(0.05))
        pygame.draw.rect(self._window, FiColor.HIGHLIGHT, pygame.Rect(x, y, w, h),  int(h/2), int(h/2))
        self.__images_counter_text.setup()
        

    def setup(self):
        self._window.fill(FiColor.BACK_COLOR)
        if time.time() - self.__timer > 4:
            self.__choose_photo()
        self.__draw_photo()
        self.__draw_photos_length()
        self.__buttons_controller.setup()
        self.__diaporama_text.setup()
        self.__transform.setup()
        
        
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()