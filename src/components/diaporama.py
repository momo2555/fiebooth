from .component_base import ComponentBase
from utils.image_utils import ImageUtils
from utils.win_utils import WinUtils
from config import config
import random as rd
import pygame
import os


class Diaporama(ComponentBase):
    MAX_FRAME = 3

    def __init__(self, window_context, w, h, x, speed : int = 7):
        super().__init__(window_context)
        self.__w = w
        self.__h = h
        self.__x = x
        self.__images = []
        self.__speed = speed


    def pick_images(self):
        self.__photos: dict = ImageUtils.get_all_user_photos_path(config.user_name)
        self.__possibilities: dict = self.__photos.copy()

        for im in self.__images:
            if im["path"] in self.__photos:
                self.__possibilities.remove(im)
        length = len(self.__possibilities)

        # delete the last image
        if self.__img_len() > 0:
            self.__images.pop()

        # add new image
        while self.__img_len() <= self.MAX_FRAME:
            error = False
            current_photo = self.__possibilities[rd.randint(0, length - 1)]
            try:
                if os.path.exists(current_photo):
                    img = pygame.image.load(current_photo).convert()
                else:
                    error = True
            except pygame.error as e:
                self._logger.warning(
                    f"Image format not supported : {current_photo}"
                )
                error = True
            if not error:
                y = -self.__h + int((self.MAX_FRAME - self.__img_len()) * self.__h * 1.08)
                self.__images.insert(
                0,
                {
                    "path": current_photo,
                    "pos": [self.__x, y],
                    "data": pygame.transform.scale(img, (self.__w, self.__h)),
                },
                )
            self.__possibilities.remove(current_photo)

    def __img_len(self) -> int:
        return len(self.__images)
    
    def __is_outside_bounds(self, img_obj) -> bool:
        return img_obj["pos"][1] > WinUtils.hprct(1)

    def setup(self):
        for im in self.__images:
            pos = (im["pos"][0], im["pos"][1])
            self._window.blit(im["data"], pos)
            im["pos"][1] = (im["pos"][1] + self.__speed)
        
        if self.__is_outside_bounds(self.__images[-1]):
            self.pick_images()
