from .stateView import StateView
from controllers.buttons_controller import ButtonsController
from controllers.test_printer import TestPrinter
from components.photo_preview import PhotoPreview
from components.text_message import TextMessage
from components.fiebooth_logo import LogoColorMode, FieboothLogo
from utils.win_utils import CenterMode
from config import config
import pygame
import time

class AskPrintView(StateView):
    def __init__(self, state_controller, window_context):
        StateView.__init__(self, state_controller, window_context, "ask_print", "printing")
        self.__photo_name : str = None
        self.__buttons_controller : ButtonsController = ButtonsController()
        self.__preview : PhotoPreview = None 
        self.__print_text : TextMessage = None
        self.__timer : float = None
        
    
    def __init_buttons(self):
        self.__buttons_controller = ButtonsController()
        self.__buttons_controller.add_button(config.green_btn, self.__yes_print, key=pygame.K_y)
        self.__buttons_controller.add_button(config.red_btn, self.__no_print, key=pygame.K_n)

    def __yes_print(self, e):
        self._logger.info(f"YES Print photo ...")
        self.set_next_state_id("printing")
        self._add_artifact("photo_name", self.__photo_name)
        self._go_next_state()

    def __no_print(self, e):
        self._logger.info(f"NO don't print photo")
        self.set_next_state_id("diaporama")
        self._go_next_state()

    def __show_preview(self):
        pass

    def show(self):
        self.__timer = time.time()
        self.__init_buttons()
        self.__photo_name = self._get_artifact("photo")
        if self.__photo_name != None:
            self.__preview = PhotoPreview(self._window, self.__photo_name)
            self.__print_text = TextMessage(self._window, "Imprimer la photo ?",
                                            center_x=CenterMode.CENTER, font_size=100,
                                            center_y=CenterMode.BOTTOM, y = 100)
        self.__logo = FieboothLogo(self._window, LogoColorMode.DARK)
    def setup(self):
        self._window.fill((255, 255, 255))
        self.__logo.setup()
        self.__buttons_controller.setup()
        if self.__photo_name != None:
            self.__preview.setup()
            self.__print_text.setup()
        else:
            self._logger.warning(f"No photo captured")
        if time.time() - self.__timer > 8:
            self.__no_print(None)
    
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()
        
