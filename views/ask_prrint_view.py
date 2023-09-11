from .stateView import StateView
from controllers.buttonsController import ButtonsController
from controllers.printer_controller import PrinterController
from controllers.test_printer import TestPrinter
from components.photo_preview import PhotoPreview
from components.text_message import TextMessage
from utils.win_utils import CenterMode
import pygame

class AskPrintView(StateView):
    def __init__(self, state_controller, window_context):
        StateView.__init__(self, state_controller, window_context, "ask_print", "camera_stream")
        self.__photo_name : str = None
        self.__buttons_controller : ButtonsController = ButtonsController()
        self.__preview : PhotoPreview = None 
        self.__print_text : TextMessage = None
        #self.__printer : PrinterController = PrinterController() 
        self.__printer : TestPrinter = TestPrinter()
    
    def __init_buttons(self):
        self.__buttons_controller.add_button(pygame.K_y, self.__yes_print)
        self.__buttons_controller.add_button(pygame.K_n, self.__no_print)

    def __yes_print(self):
        self._logger.info(f"YES Print photo ...")
        self.set_next_state_id("printing")
        self.__printer.print(self.__photo_name)
        self._go_next_state()

    def __no_print(self):
        self._logger.info(f"NO don't print photo")
        self._go_next_state()

    def __show_preview(self):
        pass

    def show(self):
        self.__init_buttons()
        self.__photo_name = self._get_artifact("photo")
        if self.__photo_name != None:
            self.__preview = PhotoPreview(self._window, self.__photo_name)
            self.__print_text = TextMessage(self._window, "Imprimer la photo ?",
                                            center_x=CenterMode.CENTER, font_size=100,
                                            center_y=CenterMode.BOTTOM, y = 100)
    
    def setup(self):
        self._window.fill((255, 255, 255))
        
        self.__buttons_controller.setup()
        if self.__photo_name != None:
            self.__preview.setup()
            self.__print_text.setup()
        else:
            self._logger.warning(f"No photo captured")
    
    def destroy(self) -> None:
        super().destroy()
        self.__buttons_controller.clear_triggers()
        