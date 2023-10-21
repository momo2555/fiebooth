from .component_base import ComponentBase
from enum import Enum
from assets.assets import get_asset_uri
import pygame
from utils.win_utils import WinUtils


class LogoColorMode(Enum):
    LIGHT = 0
    DARK = 1

class FieboothLogo(ComponentBase):
    def __init__(self, window_context, colorMode : LogoColorMode = LogoColorMode.LIGHT):
        super().__init__(window_context)
        if colorMode == LogoColorMode.LIGHT:
            logo = get_asset_uri("logo_light.png")
        else:
            logo = get_asset_uri("logo_dark.png")

        self.__img = pygame.image.load(logo).convert_alpha()
        self.__logo_size = self.__img.get_size()
        self.__reduced_size = (self.__logo_size[0]//2, self.__logo_size[1]//2)

        self.__img = pygame.transform.scale(self.__img, (self.__reduced_size[0], self.__reduced_size[1]))

    def setup(self):
        self._window.blit(self.__img, (WinUtils.wprct(0.02), WinUtils.hprct(0.98) - self.__reduced_size[1]))