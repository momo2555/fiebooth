import pygame
from .component_base import ComponentBase
from utils.win_utils import CenterMode, WinUtils
from pygame import gfxdraw
from utils.colors_utils import FiColor

class SimpleSlider(ComponentBase):
    def __init__(self, windows_context, x, y, center_x : CenterMode = None,
                 center_y: CenterMode = None, value = 0, height : int = 300,
                 width: int = 20, cursor_radius: int = 30, cursor_color = (255, 0, 0)):
        ComponentBase.__init__(self, windows_context)
        self.__value = value
        self.__center_x = center_x
        self.__center_y = center_y
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__max = 6
        self.__min = -6
        self.__cursor_color = cursor_color
        self.__cursor_radius = cursor_radius
        self.__figure_pos()

    def __figure_pos(self):
        center_pos = WinUtils.get_center_position(self.__width, self.__height)
        screen_size = WinUtils.get_screen_size()
        # X POSITION
        if self.__center_x == CenterMode.CENTER:
            self.__x = center_pos[0]
        elif self.__center_x == CenterMode.RIGHT:
            self.__x = screen_size[0] - self.__x - self.__width
        # Y position
        if self.__center_y == CenterMode.CENTER:
            self.__y = center_pos[1]
        elif self.__center_y == CenterMode.BOTTOM:
            self.__y = screen_size[1] - self.__y  - self.__height

    def set_value(self, value) -> int: 
        if value <= self.__max and value >= self.__min:
            self.__value = value
        return self.__value

    def get_value(self) -> int:
        return self.__value
    
    def plus(self) -> int:
        return self.set_value(self.__value+1)
        

    def minus(self) -> int:
        return self.set_value(self.__value-1)
        

    def setup(self):
        
        pygame.draw.rect(self._window, FiColor.BACK, (self.__x, self.__y, self.__width, self.__height))

        cursor_circle = (self.__x + self.__width // 2,
                    int(self.__y + (self.__max - self.__value) / (self.__max - self.__min) * self.__height))
        bound_circle_top = (self.__x + self.__width // 2, self.__y)
        bound_circle_bottom = (self.__x + self.__width // 2,self.__y + self.__height)

        gfxdraw.filled_circle(self._window, *bound_circle_top, self.__width//2, FiColor.BACK)
        gfxdraw.filled_circle(self._window, *bound_circle_bottom, self.__width//2, FiColor.BACK)
        gfxdraw.filled_circle(self._window, *cursor_circle, self.__cursor_radius, self.__cursor_color)
        