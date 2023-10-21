from .component_base import ComponentBase
from .text_message import TextMessage
from enum import  Enum
from config import config
from utils.win_utils import WinUtils, CenterMode
from utils.colors_utils import FiColor
from assets.assets import get_asset_uri
import pygame

class CounterType(Enum):
    PRINTS = 0
    PHOTOS = 1

class FiCounter(ComponentBase):
    def __init__(self, window_context, counter_type : CounterType, x, y, w, h):
        super().__init__(window_context)
        self.__x, self.__y = x, y
        self.__h, self.__w = h, w
        if counter_type == CounterType.PHOTOS:
            self.__text_color = FiColor.WHITE
            self.__back_color = FiColor.HIGHLIGHT
            self.__icon = get_asset_uri("photo_icon.png")
            self.__value = config.user_photos_len
        else:
            self.__text_color = FiColor.HIGHLIGHT
            self.__back_color = FiColor.WHITE
            self.__icon = get_asset_uri("print_icon.png")
            self.__value = config.user_prints_len
        
        #icon
        self.__img_icon = pygame.image.load(self.__icon).convert_alpha()
        self.__img_icon_size = (int(h*0.7), int(h*0.7))
        self.__img_icon_pos = (x + int(h*0.4), y + int(h*0.15))
        self.__img_icon = pygame.transform.scale(self.__img_icon, self.__img_icon_size)

        #counter text
        self.__counter_text = TextMessage(self._window, f"{self.__value}", color=self.__text_color,
                                            x = x + int(1.3*h),
                                            y = y + int(0.5*h), center_gravity_y=True,
                                            font_size=int(h*0.8))
    
    def setup(self) -> None:
        pygame.draw.rect(self._window, self.__back_color, pygame.Rect(self.__x, self.__y, self.__w, self.__h),  
                         int(self.__h/2), int(self.__h/2))
        self.__counter_text.setup()
        self._window.blit(self.__img_icon, self.__img_icon_pos )
