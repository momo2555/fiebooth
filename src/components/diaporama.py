from .component_base import ComponentBase
from utils.image_utils import ImageUtils
from config import config
import random as rd

class Diaporama(ComponentBase):
    def __init__(self, window_context, w, h, x):
        super().__init__(window_context)
        self.__w = w
        self.__h = h 
        self.__x = x
        self.__images = []
    
    def pick_images(self):
        self.__photos : dict = ImageUtils.get_all_user_photos_path(config.user_name)
        self.__possibilities : dict = self.__photos.copy()

        for im in self.__images:
            if im["path"] in self.__photos:
                self.__possibilities.remove(im)
        length = len(self.__possibilities)
        # delete the last image
         
        # add new image
        while len(self.__images) < 3:
            self.__images.insert(0, {
                "path" : self.__possibilities[rd.randint(0, length -1)],
                "pos" : [self.__x, ]
            })

    def __is_outside_bounds(self, img_obj):
        pass

    def setup(self):
        for im in self.__images:
            pos = (self.__photo_pos[0], self.__photo_pos[1] - WinUtils.hprct(0.5))
            self._window.blit(self.__img, pos)
            self.__photo_pos[1] = (self.__photo_pos[1]+self.__speed)%WinUtils.hprct(1.5)
            if self.__photo_pos[1] < self.__speed+1:
                self.__choose_photo()


