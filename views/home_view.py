from views.stateView import StateView
from assets.assets import get_asset_uri 
from utils.win_utils import WinUtils
from config import config
import time
import pygame


class HomeView(StateView):
    def __init__(self, state_controller, window_context):
        StateView.__init__(self, state_controller, window_context, "home", "diaporama")
        self.__timer = 0

    def show(self):
        self.__timer = time.time()
        pass

    def setup(self):
        if(time.time() - self.__timer < config.home_delay):
            load = pygame.image.load(get_asset_uri("accueil.jpg")).convert_alpha()

            image = pygame.transform.scale(load, WinUtils.get_screen_size())
            self._window.blit(image,(0,0))
        else:
            self._go_next_state()