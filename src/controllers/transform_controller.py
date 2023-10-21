from components.simple_slider import SimpleSlider
from utils.win_utils import WinUtils, CenterMode
from utils.image_utils import ImageUtils
from config import config, Config
from components.diaporama import Diaporama
import pygame
import time

class TransformController():
    def __init__(self, window_context, preview_path):
        self.__window = window_context
        self.__preview = None
        self.__contr_value = config.contrast
        self.__bright_value = config.brightness
        self.__contr_slider = SimpleSlider(self.__window, x = WinUtils.wprct(0.1), y = WinUtils.hprct(0.1),
                                           width=WinUtils.wprct(0.04), center_y=CenterMode.CENTER,
                                           cursor_radius=WinUtils.wprct(0.03), cursor_color=(255, 0, 0),
                                           height=WinUtils.hprct(0.75), value=self.__contr_value)
        self.__bright_slider = SimpleSlider(self.__window, x = WinUtils.wprct(0.1), y = WinUtils.hprct(0.1),
                                           width=WinUtils.wprct(0.04), center_y=CenterMode.CENTER,
                                           cursor_radius=WinUtils.wprct(0.03), cursor_color=(0, 255, 0),
                                           center_x=CenterMode.RIGHT, height=WinUtils.hprct(0.75),
                                           value=self.__bright_value)
        self.__tf_path = preview_path
        self.__update_transform()
        
        self.__show_contr = False
        self.__show_bright = False
        self.__timer = 0
    
    def setup(self, diaporama : Diaporama = None):
        if (self.__show_bright or self.__show_contr):
            if diaporama is not None:
                diaporama.pause()
            self.__draw_background()
            self.__window.blit(self.__tf, 
                            WinUtils.get_center_position(WinUtils.wprct(0.5), WinUtils.hprct(0.5)))

        if (self.__show_contr):self.__contr_slider.setup()
        if (self.__show_bright):self.__bright_slider.setup()
        
        if (time.time() - self.__timer > 2):
            self.__show_contr = False
            self.__show_bright = False
            if diaporama is not None:
                diaporama.play()

    def __update_transform(self):
        config["contrast"] = self.__contr_value
        config["brightness"] = self.__bright_value
        contrast = 1 + (self.__contr_value)/6
        brightness = 1 + (self.__bright_value)/6
        self.__tf = ImageUtils.image_transform_pyg(self.__tf_path, contrast=contrast, brightness=brightness,
                                               scale=(WinUtils.wprct(0.5), WinUtils.hprct(0.5)),
                                               user_text=config.user_text)
    
    def __draw_background(self):
        background = pygame.Surface(WinUtils.get_screen_size(), pygame.SRCALPHA)   # per-pixel alpha
        background.fill((220,220,220,170))                         # notice the alpha value in the color
        self.__window.blit(background, (0,0))

    def contrast_up(self):
        self.__contr_value=self.__contr_slider.plus()
        self.__timer = time.time()
        self.__show_contr = True
        self.__update_transform()

    def contrast_down(self):
        self.__contr_value=self.__contr_slider.minus()
        self.__timer = time.time()
        self.__show_contr = True
        self.__update_transform()

    def brightness_up(self):
        self.__bright_value= self.__bright_slider.plus()
        self.__timer = time.time()
        self.__show_bright = True
        self.__update_transform()

    def brightness_down(self):
        self.__bright_value= self.__bright_slider.minus()
        self.__timer = time.time()
        self.__show_bright = True
        self.__update_transform()