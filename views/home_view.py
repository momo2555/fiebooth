from views.stateView import StateView
from assets.assets import get_asset_uri 
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
        if(time.time() - self.__timer < config.HOME_DELAY):
            load = pygame.image.load(get_asset_uri("accueil.jpg")).convert_alpha()
            image = pygame.transform.scale(load,(config.WIDTH_DISPLAY,config.HEIGHT_DISPLAY))
            self._window.blit(image,(0,0))
        else:
            self._go_next_state()