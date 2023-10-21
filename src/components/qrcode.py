from .component_base import ComponentBase
from utils.colors_utils import FiColor
import qrcode
from enum import Enum
from utils.wifi_utils import WifiUtils
import pygame
from pathlib import Path
from utils.file_utils import FileUtils
from utils.win_utils import WinUtils


class QrType(Enum):
    URL = 0,
    WIFI = 0


# the qr code is positionned from his center
class FiQrcode(ComponentBase):
    def __init__(self, window, type : QrType, value : str = "", x : int = 0, y : int = 0, h : int = 200, w : int = 200):
        self.__type = type
        self.__value = value
        self.__x = x
        self.__y = y
        self.__h = h
        self.__w = w
        self._window = window
        self.__img_path = Path(FileUtils.get_temp_dir(), f"qr_{self.__type.name}.png")
        self.__create_the_qrcode()

    def __create_the_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        data = self.__value
        if self.__type == QrType.WIFI:
            ssid = WifiUtils.get_ssid()
            password = WifiUtils.get_password()
            data = f"WIFI:T:PWA;S:{ssid};P:{password};;"
        elif self.__value == "":
            data = "http://portail.fiebooth"

        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=FiColor.DARK, back_color=FiColor.WHITE)
        img.save(self.__img_path)
        
        py_img = pygame.image.load(self.__img_path).convert()
        self.__py_img = pygame.transform.scale(py_img, (self.__w, self.__h))

    def set_x(self, value):
        self.__x = value

    def set_y(self, value):
        self.__y = value

    def setup(self) -> None:
        #draw the surarounded sqaure
        (sw, sh) = (int(self.__w*1.08), int(self.__h*1.08))
        (sx, sy) = (self.__x - int(sw/2), self.__y - int(sh/2))
        pygame.draw.rect(self._window, FiColor.WHITE, pygame.Rect(sx, sy, sw, sh),  int(sh/2), 30)
        
        #draw the qrcode
        (w, h) = (self.__w, self.__h)
        (x, y) = (self.__x - int(w/2), self.__y - int(h/2))
        self._window.blit(self.__py_img, (x, y))