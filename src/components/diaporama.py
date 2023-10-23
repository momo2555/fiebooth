from .component_base import ComponentBase
from utils.image_utils import ImageUtils
from utils.win_utils import WinUtils
from config import config
from assets.assets import get_asset_uri
import random as rd
import pygame
import os


class Diaporama(ComponentBase):
    MAX_FRAME = 4

    def __init__(self, window_context, w, h, x, speed : int = 4):
        super().__init__(window_context)
        self.__w = w
        self.__h = h
        self.__x = x
        self.__images = []
        self.__speed = speed
        self.__gap = WinUtils.hprct(0.05)
        self.__running = True
        self.pick_images()


    def pick_images(self):
        self.__photos: dict = ImageUtils.get_all_user_photos_path(config.user_name)
        self.__possibilities: dict = self.__photos.copy()

        for im in self.__images:
            if im["path"] in self.__photos:
                self.__possibilities.remove(im["path"])
        

        # delete the last image
        if self.__img_len() > 0:
            self.__images.pop()

        length = len(self.__possibilities)
        # add new image
        while self.__img_len() < self.MAX_FRAME:
            error = False
            if length > 0:
                current_photo = self.__possibilities[rd.randint(0, length - 1)]
            else:
                current_photo = get_asset_uri("accueil.jpg")
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
                y = -self.__h + int((self.MAX_FRAME - 1 - self.__img_len()) * (self.__h + self.__gap))
                self.__images.insert(
                0,
                {
                    "path": current_photo,
                    "pos": [self.__x, y],
                    "data": pygame.transform.scale(img, (self.__w, self.__h)),
                },
                )
            self.__remove_possibility(current_photo)
            length = len(self.__possibilities)

    def __img_len(self) -> int:
        return len(self.__images)
    
    def __is_outside_bounds(self, img_obj) -> bool:
        return img_obj["pos"][1] > self.__gap

    def __remove_possibility(self, photo):
        try:
            self.__possibilities.remove(photo)
        except ValueError as e:
            self._logger.warning(f"can't remove {photo}, it'is not a possibility.")
    def pause(self):
        self.__running = False
    
    def play(self):
        self.__running = True

    def setup(self):
        for im in self.__images:
            pos = (im["pos"][0], im["pos"][1])
            self._window.blit(im["data"], pos)
            if self.__running:
                im["pos"][1] = (im["pos"][1] + self.__speed)
        
        if self.__is_outside_bounds(self.__images[0]):
            self.pick_images()
