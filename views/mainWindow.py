import pygame
from config import config

class MainWindow:
    def __init__(self):
        pygame.init()	#init library
        pygame.display.set_caption(config.APP_NAME)
        self.window = pygame.display.set_mode((config.WIDTH_DISPLAY,config.HEIGHT_DISPLAY),pygame.FULLSCREEN)
        pass

    def setup(self):
        events = pygame.event.get()
        for event in events:
                if event.type == pygame.KEYDOWN:
                    print("window: button pressed")

        load = pygame.image.load("accueil.jpg").convert_alpha()
        image = pygame.transform.scale(load,(config.WIDTH_DISPLAY,config.HEIGHT_DISPLAY))
        self.window.blit(image,(0,0))
        #skip_button.draw(screen)    #print SKIP button
        #quit_button.draw(screen) 

        pygame.time.delay(10)
        pygame.display.update()
        pass