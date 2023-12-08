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
from components.fiebooth_logo import FieboothLogo, LogoColorMode
from components.counter import FiCounter, CounterType
from config import config
import random as rd
from assets.assets import get_asset_uri
from utils.colors_utils import FiColor
from components.qrcode import FiQrcode, QrType


class DiaporamaView(StateView):
    def __init__(self, state_controller, window_context, camera):
        StateView.__init__(self, state_controller, window_context, "diaporama", "countdown")
        self.__camera : CameraController = camera
        self.__buttons_controller : ButtonsController = ButtonsController()
        self.__photos = []
        self.__current_photo : str = None
        self.__transform : TransformController = None

    def __init_buttons_events(self):
        self.__buttons_controller = ButtonsController()
        self.__buttons_controller.add_button(config.green_btn, self.__trigger_shot_callback, key=pygame.K_a)
        self.__buttons_controller.add_button(1, self.__config_contrast_up, key=pygame.K_UP)
        self.__buttons_controller.add_button(2, self.__config_contrast_down, key=pygame.K_DOWN)
        self.__buttons_controller.add_button(3, self.__config_brightness_up, key=pygame.K_RIGHT)
        self.__buttons_controller.add_button(4, self.__config_brightness_down, key=pygame.K_LEFT)

    def __trigger_shot_callback(self, e):
        self._logger.info("Shot button triggered !")
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

    def show(self):
        self.__init_buttons_events()
        self.__choose_photo()
        self.__transform = TransformController(self._window, self.__current_photo)
        self.__images_counter = FiCounter(self._window, CounterType.PHOTOS, 
                                          x=WinUtils.wprct(0.03), y=WinUtils.hprct(0.05),
                                          w=WinUtils.wprct(0.13), h=WinUtils.hprct(0.065))
        self.__prints_counter = FiCounter(self._window, CounterType.PRINTS, 
                                          x=WinUtils.wprct(0.19), y=WinUtils.hprct(0.05),
                                          w=WinUtils.wprct(0.13), h=WinUtils.hprct(0.065))
        self.__diaporama = Diaporama(self._window, w=WinUtils.wprct(0.55), h=WinUtils.hprct(0.55),
                                     x=WinUtils.wprct(0.4))
       
        self.__wifi_text = TextMessage(self._window, "1) Se connecter au WIFI Fiebooth", color=FiColor.WHITE,
                                            x = WinUtils.wprct(0.35/2), center_gravity_x=True,
                                            y = WinUtils.hprct(0.19), center_gravity_y=True,
                                            font_size=WinUtils.hprct(0.035))
        self.__wifi_qr = FiQrcode(self._window, QrType.WIFI, x=WinUtils.wprct(0.35/2), y=WinUtils.hprct(0.37),
                                  h=WinUtils.hprct(0.25), w=WinUtils.hprct(0.25))
        self.__url_text = TextMessage(self._window, "2) Accéder au portail Fiebooth", color=FiColor.WHITE,
                                            x = WinUtils.wprct(0.35/2), center_gravity_x=True,
                                            y = WinUtils.hprct(0.54), center_gravity_y=True,
                                            font_size=WinUtils.hprct(0.035))
        self.__url_qr = FiQrcode(self._window, QrType.URL, x=WinUtils.wprct(0.35/2), y=WinUtils.hprct(0.72),
                                 h=WinUtils.hprct(0.25), w=WinUtils.hprct(0.25))
        self.__user_text =  TextMessage(self._window, f"{config.user_name}", color=FiColor.WHITE,
                                        x = WinUtils.wprct(0.67), center_x=CenterMode.RIGHT,
                                        y = WinUtils.hprct(0.02), center_y=CenterMode.BOTTOM,
                                        font_size=WinUtils.hprct(0.04))
        self.__logo = FieboothLogo(self._window)
        
    
    def __draw_wifi_qrcode(self):
        self.__wifi_text.setup()
        self.__wifi_qr.setup()   

    def __draw_url_qrcode(self):
        self.__url_qr.setup()
        self.__url_text.setup()
    
    def __draw_background(self):
        self._window.fill(FiColor.BACK)
        pygame.draw.rect(self._window, FiColor.SURFACE, (WinUtils.wprct(0.35), 0, 
                                                         WinUtils.wprct(0.65), WinUtils.hprct(1)))

    def setup(self):
        self.__draw_background()
        # self.__draw_photos_length()
        self.__images_counter.setup()
        self.__prints_counter.setup()
        self.__buttons_controller.setup()
        self.__draw_wifi_qrcode()
        self.__draw_url_qrcode()
        self.__diaporama.setup()
        self.__logo.setup()
        self.__user_text.setup()
        self.__transform.setup(self.__diaporama)
        
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()