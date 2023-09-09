import pygame
from enum import Enum

class CenterMode(Enum):
    CENTER = 0
    RIGHT = BOTTOM = 1
    LEFT = TOP = 2



class WinUtils:
    @staticmethod
    def get_screen_size() -> tuple:
        return pygame.display.get_surface().get_size()
    
    @staticmethod
    def get_center_position(width, height):
        screen_w, screen_h = WinUtils.get_screen_size()
        x_pos = int((screen_w - width)/2)
        y_pos = int((screen_h - height)/2)
        return x_pos, y_pos

    def screen_prct_width(prct: float) -> int:
        return int(WinUtils.get_screen_size()[0] * prct)
    
    def screen_prct_height(prct: float) -> int:
        return int(WinUtils.get_screen_size()[1] * prct)