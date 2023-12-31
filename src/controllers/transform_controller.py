from components.simple_slider import SimpleSlider
from utils.win_utils import WinUtils, CenterMode
from utils.image_utils import ImageUtils
from utils.colors_utils import FiColor
from config import config, Config
from components.diaporama import Diaporama
from components.text_message import TextMessage
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
                                           cursor_radius=WinUtils.wprct(0.03), cursor_color=FiColor.BLUE,
                                           height=WinUtils.hprct(0.75), value=self.__contr_value)
        self.__bright_slider = SimpleSlider(self.__window, x = WinUtils.wprct(0.1), y = WinUtils.hprct(0.1),
                                           width=WinUtils.wprct(0.04), center_y=CenterMode.CENTER,
                                           cursor_radius=WinUtils.wprct(0.03), cursor_color=FiColor.YELLOW,
                                           center_x=CenterMode.RIGHT, height=WinUtils.hprct(0.75),
                                           value=self.__bright_value)
        self.__transform_text =  TextMessage(self.__window, f" ", color=FiColor.DARK,
                                        center_x=CenterMode.CENTER,
                                        y = WinUtils.hprct(0.1125), center_y=CenterMode.BOTTOM, center_gravity_y=True,
                                        font_size=WinUtils.hprct(0.1))
        self.__plus_contr =  TextMessage(self.__window, f"+", color=FiColor.GREEN,
                                        x=WinUtils.wprct(0.12), center_gravity_x=True,
                                        y=WinUtils.hprct(0.05), center_gravity_y=True,
                                        font_size=WinUtils.hprct(0.15))
        self.__plus_bright =  TextMessage(self.__window, f"+", color=FiColor.GREEN,
                                        x=WinUtils.wprct(0.12), center_gravity_x=True, center_x=CenterMode.RIGHT,
                                        y=WinUtils.hprct(0.05), center_gravity_y=True,
                                        font_size=WinUtils.hprct(0.15))
        self.__min_contr =  TextMessage(self.__window, f"-", color=FiColor.RED,
                                        x=WinUtils.wprct(0.12), center_gravity_x=True,
                                        y=WinUtils.hprct(0.05), center_gravity_y=True, center_y=CenterMode.BOTTOM,
                                        font_size=WinUtils.hprct(0.15))
        self.__min_bright =  TextMessage(self.__window, f"-", color=FiColor.RED,
                                        x=WinUtils.wprct(0.12), center_gravity_x=True, center_x=CenterMode.RIGHT,
                                        y=WinUtils.hprct(0.05), center_gravity_y=True, center_y=CenterMode.BOTTOM,
                                        font_size=WinUtils.hprct(0.15))
        
        self.__tf_path = preview_path
        self.__update_transform()
        
        self.__show_contr = False
        self.__show_bright = False
        self.__timer = 0
    
    def __setup_contr_buttons(self):
        self.__min_contr.setup()
        self.__plus_contr.setup()
    
    def __setup_bright_buttons(self):
        self.__min_bright.setup()
        self.__plus_bright.setup()

    def setup(self, diaporama : Diaporama = None):
        if (self.__show_bright or self.__show_contr):
            if diaporama is not None:
                diaporama.pause()
            self.__draw_background()
            self.__window.blit(self.__tf, 
                            WinUtils.get_center_position(WinUtils.wprct(0.5), WinUtils.hprct(0.5)))
            self.__transform_text.setup()

        if (self.__show_contr):
            self.__contr_slider.setup()
            self.__setup_contr_buttons()
        if (self.__show_bright):
            self.__bright_slider.setup()
            self.__setup_bright_buttons()
        
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
        background.fill((250,250,250,210))                         # notice the alpha value in the color
        self.__window.blit(background, (0,0))

    def contrast_up(self):
        self.__contr_value=self.__contr_slider.plus()
        self.__timer = time.time()
        self.__show_contr = True
        self.__transform_text.set_text("Contraste")
        self.__update_transform()

    def contrast_down(self):
        self.__contr_value=self.__contr_slider.minus()
        self.__timer = time.time()
        self.__show_contr = True
        self.__transform_text.set_text("Contraste")
        self.__update_transform()

    def brightness_up(self):
        self.__bright_value= self.__bright_slider.plus()
        self.__timer = time.time()
        self.__show_bright = True
        self.__transform_text.set_text("Luminosité")
        self.__update_transform()

    def brightness_down(self):
        self.__bright_value= self.__bright_slider.minus()
        self.__timer = time.time()
        self.__show_bright = True
        self.__transform_text.set_text("Luminosité")
        self.__update_transform()