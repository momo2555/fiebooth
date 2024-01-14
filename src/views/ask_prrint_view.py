from .stateView import StateView
from controllers.buttons_controller import ButtonsController
from controllers.test_printer import TestPrinter
from components.photo_preview import PhotoPreview
from components.text_message import TextMessage
from components.fiebooth_logo import LogoColorMode, FieboothLogo
from utils.win_utils import CenterMode, WinUtils
from utils.colors_utils import FiColor
from config import config
from pygame import gfxdraw
import pygame
import time

class AskPrintView(StateView):
    def __init__(self, state_controller, window_context, button : ButtonsController):
        StateView.__init__(self, state_controller, window_context, "ask_print", "printing")
        self.__photo = None
        self.__buttons_controller : ButtonsController = button
        self.__preview : PhotoPreview = None 
        self.__print_text : TextMessage = None
        self.__timer : float = None
        
    
    def __init_buttons(self):
        #self.__buttons_controller = ButtonsController()
        self.__buttons_controller.add_button(config.green_btn, self.__yes_print, key=pygame.K_y)
        self.__buttons_controller.add_button(config.red_btn, self.__no_print, key=pygame.K_n)

    def __yes_print(self, e):
        self._logger.info(f"YES Print photo ...")
        self.set_next_state_id("printing")
        self._add_artifact("photo", self.__photo)
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
        self.__photo = self._get_artifact("photo")
        if self.__photo != None:
            self.__preview = PhotoPreview(self._window, self.__photo[1])
            self.__print_text = TextMessage(self._window, "Imprimer la photo ?",
                                            center_x=CenterMode.CENTER, font_size=100,
                                            center_y=CenterMode.BOTTOM, y = 100)
        self.__logo = FieboothLogo(self._window, LogoColorMode.DARK)
        self.__yes = TextMessage(self._window, "OUI", color=FiColor.WHITE,
                                 font_size=100, x=WinUtils.wprct(0.1125), center_gravity_x=True,
                                 center_y=CenterMode.CENTER,)
        self.__no = TextMessage(self._window, "NON", color=FiColor.WHITE,
                                 font_size=100, x=WinUtils.wprct(0.8875), center_gravity_x=True,
                                 center_y=CenterMode.CENTER,)
    
    def __draw_yes_no_indicators(self):
        yes_circle = (WinUtils.wprct(0.1125), WinUtils.hprct(0.5))
        no_circle = (WinUtils.wprct(0.8875), WinUtils.hprct(0.5))

        gfxdraw.filled_circle(self._window, *no_circle, WinUtils.wprct(0.07), FiColor.RED)
        gfxdraw.filled_circle(self._window, *yes_circle, WinUtils.wprct(0.07), FiColor.GREEN)

        self.__yes.setup()
        self.__no.setup()

    def setup(self):
        self._window.fill((255, 255, 255))
        
        if not self.__photo is None:
            self.__preview.setup()
            self.__print_text.setup()
        else:
            self._logger.warning(f"No photo captured")
        if time.time() - self.__timer > 8:
            self.__no_print(None)
        self.__logo.setup()

        self.__draw_yes_no_indicators()
        self.__buttons_controller.setup()
        
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()
        
