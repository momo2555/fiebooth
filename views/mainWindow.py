import pygame
import config

class MainWindow:
    def __init__(self):
        pygame.init()	#init library
        pygame.display.set_caption(config.APP_NAME)
        self.window = pygame.display.set_mode((config.WIDTH_DISPLAY,config.HEIGHT_DISPLAY),pygame.FULLSCREEN)
        pass

    def setup(self):
        pass