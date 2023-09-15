import pygame
from .component_base import CompenentBase
from utils.win_utils import CenterMode, WinUtils
from pygame import gfxdraw

class SimpleSlider(CompenentBase):
    def __init__(self, windows_context, x, y, center_x : CenterMode = None,
                 center_y: CenterMode = None, value = 0, height : int = 300,
                 width: int = 20):
        CompenentBase.__init__(self, windows_context)
        self.__value = 0
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__max = 6
        self.__min = -6

    def set_value(self, value): 
        self.__value = value
    def get_value(self):
        return self.__value

    def setup(self):
        
        pygame.draw.rect(self._window, (200,200,200), (self.__x, self.__y, self.__width, self.__height))

        #if self.vertical:
        # if self.curved:
        #     pygame.draw.circle(self._window, (255, 0, 0), (self.__x + self.__width // 2, self.__y), 30)
        #     pygame.draw.circle(self.win, self.colour, (self._x + self._width // 2, self._y + self._height),
        #                         self.radius)
        circle = (self.__x + self.__width // 2,
                    int(self.__y + (self.__max - self.__value) / (self.__max - self.__min) * self.__height))
        # else:
        #     if self.curved:
        #         pygame.draw.circle(self.win, self.colour, (self._x, self._y + self._height // 2), self.radius)
        #         pygame.draw.circle(self.win, self.colour, (self._x + self._width, self._y + self._height // 2),
        #                            self.radius)
        #     circle = (int(self._x + (self.value - self.min) / (self.max - self.min) * self._width),
        #               self._y + self._height // 2)

        gfxdraw.filled_circle(self._window, *circle, 30, (255, 0, 0))
        gfxdraw.aacircle(self._window, *circle, 30, (255, 0, 0))