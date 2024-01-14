from .component_base import ComponentBase
from utils.win_utils import WinUtils
import pygame
from typing import Any
from PIL import Image

class PhotoPreview(ComponentBase):
    def __init__(self, window_context, image : Any):
        ComponentBase.__init__(self, window_context)
        image = Image.fromarray(image)
        mode = image.mode 
        size = image.size 
        data = image.tobytes() 

        self.__img = pygame.image.fromstring(data, size, mode).convert()
        self.__def_width, self.__def_height = self.__img.get_size()
        self.__w = WinUtils.wprct(1)
        self.__h = WinUtils.hprct(1)
        self.__img = pygame.transform.scale(self.__img, 
                                            (self.__w, self.__h))
        
    
    def setup(self):
        position = (WinUtils.get_center_position(self.__w, self.__h)[0],
                    0)
        self._window.blit(self.__img, position)
