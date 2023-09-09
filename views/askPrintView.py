from .stateView import StateView
from controllers.buttonsController import ButtonsController
import pygame

class AskPrintView(StateView):
    def __init__(self, state_controller, window_context):
        StateView.__init__(self, state_controller, window_context, "ask_print", "camera_stream")
        self.__photo_name : str = None
        self.__buttons_controller : ButtonsController = ButtonsController()
    
    def __init_buttons(self):
        self.__buttons_controller.add_button(pygame.K_y, self.__yes_print)
        self.__buttons_controller.add_button(pygame.K_n, self.__no_print)

    def __yes_print(self):
        self._logger.info(f"YES Print photo ...")
        self._go_next_state()

    def __no_print(self):
        self._logger.info(f"NO don't print photo ...")
        self._go_next_state()

    def show(self):
        self.__init_buttons()
        self.__photo_name = self._get_artifact("photo")
    
    def setup(self):
        self.__buttons_controller.setup()
        if self.__photo_name != None:
            pass
        else:
            self._logger.warning(f"No photo captured")
    
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()
        