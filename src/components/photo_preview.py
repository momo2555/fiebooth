from .component_base import ComponentBase
from utils.win_utils import WinUtils
import pygame

class PhotoPreview(ComponentBase):
    def __init__(self, window_context, image_path):
        ComponentBase.__init__(self, window_context)
        self.__img = pygame.image.load(image_path).convert()
        self.__def_width, self.__def_height = self.__img.get_size()
        self.__w = WinUtils.wprct(0.55)
        self.__h = WinUtils.hprct(0.55)
        self.__img = pygame.transform.scale(self.__img, 
                                            (self.__w, self.__h))
        
    
    def setup(self):
        position = (WinUtils.get_center_position(self.__w, self.__h)[0],
                    150)
        self._window.blit(self.__img, position)
