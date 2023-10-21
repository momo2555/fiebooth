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
from components.diaporama import Diaporama
from config import config
import random as rd
import time
from assets.assets import get_asset_uri
import os
from utils.colors_utils import FiColor
import qrcode
import PIL.Image
from components.qrcode import FiQrcode, QrType

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
    
    def __choose_photo(self):
        self.__photos = ImageUtils.get_all_user_photos_path(config.user_name)
        length = len(self.__photos)
        if length > 0:
            self.__current_photo = self.__photos[rd.randint(0, length -1)]
        else:
            self.__current_photo = get_asset_uri("accueil.jpg")
        # self.__timer = time.time()

        # try:
        #     if os.path.exists(self.__current_photo):
        #         self.__img = pygame.image.load(self.__current_photo).convert()
        #     else:
        #         self.__choose_photo()
        # except pygame.error as e:
        #     self._logger.warning(f"Image format not supported : {self.__current_photo}")
        # (sw, sh) = (WinUtils.wprct(0.39), WinUtils.hprct(0.39))
        # self.__img = pygame.transform.scale(self.__img, (sw, sh))



    def show(self):
        self.__init_buttons_events()
        self.__choose_photo()
        self.__transform = TransformController(self._window, self.__current_photo)
        self.__diaporama_text = TextMessage(self._window, "Diaporama", color=FiColor.HIGHLIGHT,
                                            x = WinUtils.wprct(0.1),
                                            y = WinUtils.hprct(0.1),
                                            center_y=CenterMode.BOTTOM, font_size=WinUtils.hprct(0.06))
        self.__diaporama = Diaporama(self._window, w=WinUtils.wprct(0.4), h=WinUtils.hprct(0.4),
                                     x=WinUtils.wprct(0.55))
        self.__images_counter_text = TextMessage(self._window, f"{config.user_photos_len}", color=FiColor.WHITE,
                                            x = WinUtils.wprct(0.07),
                                            y = WinUtils.hprct(0.053),
                                            center_y=CenterMode.TOP, font_size=WinUtils.hprct(0.06))
        self.__wifi_text = TextMessage(self._window, "1) Se connecter au WIFI Fiebooth", color=FiColor.WHITE,
                                            x = WinUtils.wprct(0.1),
                                            y = WinUtils.hprct(0.17),
                                            center_y=CenterMode.TOP, font_size=WinUtils.hprct(0.04))
        self.__wifi_qr = FiQrcode(self._window, QrType.WIFI, x=WinUtils.wprct(0.25), y=WinUtils.hprct(0.37),
                                  h=WinUtils.hprct(0.25), w=WinUtils.hprct(0.25))
        self.__url_text = TextMessage(self._window, "2) Accéder au portail Fiebooth", color=FiColor.WHITE,
                                            x = WinUtils.wprct(0.1),
                                            y = WinUtils.hprct(0.52),
                                            center_y=CenterMode.TOP, font_size=WinUtils.hprct(0.04))
        self.__url_qr = FiQrcode(self._window, QrType.URL, x=WinUtils.wprct(0.25), y=WinUtils.hprct(0.72),
                                 h=WinUtils.hprct(0.25), w=WinUtils.hprct(0.25))

    # def __draw_photo(self):
    #     pos = (self.__photo_pos[0], self.__photo_pos[1] - WinUtils.hprct(0.5))
    #     self._window.blit(self.__img, pos)
    #     self.__photo_pos[1] = (self.__photo_pos[1]+self.__speed)%WinUtils.hprct(1.5)
    #     if self.__photo_pos[1] < self.__speed+1:
    #         self.__choose_photo()
    
    def __draw_wifi_qrcode(self):
        
        
        self.__wifi_text.setup()
        self.__wifi_qr.setup()   

    def __draw_url_qrcode(self):
        
        self.__url_qr.setup()
        self.__url_text.setup()
        
    def __draw_photos_length(self):
        (w, h) = (WinUtils.wprct(0.13), WinUtils.hprct(0.08))
        (x, y) = (WinUtils.wprct(0.05), WinUtils.hprct(0.05))
        pygame.draw.rect(self._window, FiColor.HIGHLIGHT, pygame.Rect(x, y, w, h),  int(h/2), int(h/2))
        self.__images_counter_text.setup()
        
    def setup(self):
        self._window.fill(FiColor.BACK)
        #if time.time() - self.__timer > 4:
        #    self.__choose_photo()
        # self.__draw_photo()
        self.__draw_photos_length()
        self.__buttons_controller.setup()
        #self.__diaporama_text.setup()
        self.__draw_wifi_qrcode()
        self.__draw_url_qrcode()
        self.__diaporama.setup()
        self.__transform.setup(self.__diaporama)
        
        
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()