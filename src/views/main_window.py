import pygame
from views.home_view import HomeView
from views.camera_stream_view import CameraStreamView
from views.countdown_view import CountDownView
from views.ask_prrint_view import AskPrintView
from views.printing_view import PrintingView
from views.blank_smile_view import BlankSmileView
from views.diaporama_view import DiaporamaView
from controllers.stateMachineController import StateMachineController
from controllers.buttons_controller import ButtonsController
from controllers.camera_controller import CameraController
from controllers.flash_controller import FlashController
from config import config
import logging


class MainWindow:
    def __init__(self, connection):
        pygame.init()	#init library
        pygame.display.set_caption(config.app_name)
        self.__window = pygame.display.set_mode(flags = pygame.FULLSCREEN)
        self.__conn = connection

        self.__logger = logging.getLogger("fiebooth")
        self.__state_machine = StateMachineController(self.__conn)
        self.__camera : CameraController = CameraController()
        self.__button_controller : ButtonsController = ButtonsController()
        self.__flash_controller : FlashController = FlashController()
        self.__camera.start()
        self.__init_state_machine()

    def __init_state_machine(self):
        self.__logger.info(f"Init state machine")

        home_state = HomeView(self.__state_machine, self.__window)
        #camera_stream_state = CameraStreamView(self.__state_machine, self.__window, self.__camera)
        diaporama_state = DiaporamaView(self.__state_machine, self.__window, self.__camera, self.__button_controller)
        countdown_state = CountDownView(self.__state_machine, self.__window, self.__camera)
        blank_smile = BlankSmileView(self.__state_machine, self.__window, self.__camera, self.__flash_controller)
        ask_print_state = AskPrintView(self.__state_machine, self.__window, self.__button_controller)
        printing_view = PrintingView(self.__state_machine, self.__window)
        self.__state_machine.add_state(home_state)
        self.__state_machine.add_state(diaporama_state)
        self.__state_machine.add_state(countdown_state)
        self.__state_machine.add_state(blank_smile)
        self.__state_machine.add_state(ask_print_state)
        self.__state_machine.add_state(printing_view)


    def setup(self): 
        self.__state_machine.setup()
        pygame.time.delay(5)
        pygame.display.update()
    