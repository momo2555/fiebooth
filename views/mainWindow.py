import pygame
from views.homeView import HomeView
from views.cameraStreamView import CameraStreamView
from views.countdownView import CountDownView
from views.askPrintView import AskPrintView
from controllers.stateMachineController import StateMachineController
from controllers.buttonsController import ButtonsController
from controllers.cameraController import CameraController
from config import config
import logging


class MainWindow:
    def __init__(self):
        pygame.init()	#init library
        pygame.display.set_caption(config.APP_NAME)
        self.__window = pygame.display.set_mode(flags = pygame.FULLSCREEN)
        #self.__screen_width, self.__screen_height = self.__window.display.get_size()

        self.__logger = logging.getLogger("fiebooth")
        self.__state_machine = StateMachineController()
        self.__camera : CameraController = CameraController()
        self.__camera.start()
        self.__init_state_machine()
        
    def __init_state_machine(self):
        self.__logger.info(f"Init state machine")
        home_state = HomeView(self.__state_machine, self.__window)
        camera_stream_state = CameraStreamView(self.__state_machine, self.__window, self.__camera)
        countdown_state = CountDownView(self.__state_machine, self.__window, self.__camera)
        ask_print_state = AskPrintView(self.__state_machine, self.__window)
        self.__state_machine.add_state(home_state)
        self.__state_machine.add_state(camera_stream_state)
        self.__state_machine.add_state(countdown_state)
        self.__state_machine.add_state(ask_print_state)
        pass


    def setup(self): 
        self.__state_machine.setup()
        pygame.time.delay(10)
        pygame.display.update()
        pass