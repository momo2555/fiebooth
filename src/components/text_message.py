from .component_base import ComponentBase
from assets.assets import get_asset_uri
from utils.win_utils import CenterMode, WinUtils
import pygame

class TextMessage(ComponentBase):
    def __init__(self, window_context, text, x = 0, y = 0, 
                 center_x = None, center_y = None, 
                 color = (0,0,0), font_size = 30,
                 center_gravity_x:bool=False, center_gravity_y:bool=False):
        ComponentBase.__init__(self, window_context)
        self.__text = text
        self.__font = pygame.font.Font(get_asset_uri("BradBunR.ttf"), font_size)
        self.__color = color
        self.__x = x
        self.__y = y
        self.__center_x = center_x
        self.__center_y = center_y
        self.__center_gravity_x = center_gravity_x
        self.__center_gravity_y = center_gravity_y
        self.__figure_position()

    def get_render_size(self):
        return self.__font.render(self.__text, True, self.__color).get_size()
    
    def __figure_position(self):
        temp_size = self.get_render_size()
        center_pos = WinUtils.get_center_position(*temp_size)
        screen_size = WinUtils.get_screen_size()
        # X POSITION
        gravity_sign = [1, 1]
        if self.__center_x == CenterMode.CENTER:
            self.__x = center_pos[0]
        elif self.__center_x == CenterMode.RIGHT:
            self.__x = screen_size[0] - self.__x - temp_size[0]
            gravity_sign[0] = -1
        # Y position
        if self.__center_y == CenterMode.CENTER:
            self.__y = center_pos[1]
        elif self.__center_y == CenterMode.BOTTOM:
            self.__y = screen_size[1] - self.__y  - temp_size[1]
            gravity_sign[1] = -1

        if self.__center_gravity_x:
            self.__x -= gravity_sign[0]*temp_size[0] //2
        if self.__center_gravity_y:
            self.__y -= gravity_sign[1]*temp_size[1] //2

    def setup(self) -> None:
        img = self.__font.render(self.__text, True, self.__color)
        self._window.blit(img, (self.__x, self.__y))
        pass

    def set_text(self, text : str) -> None:
        self.__text = text