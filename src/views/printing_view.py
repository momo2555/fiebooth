from .stateView import StateView
from assets.assets import get_asset_uri
from controllers.cameraController import CameraController
from utils.camera_utils import CameraUtils
from utils.win_utils import CenterMode
from utils.colors_utils import FiColor
from controllers.test_printer import TestPrinter
from components.text_message import TextMessage
import time
import pygame

class PrintingView(StateView):
    def __init__(self, state_controller, window_context):
        StateView.__init__(self, state_controller, window_context, "printing", "diaporama")
        self.__printer : TestPrinter = None
        self.__timer : int = 0
        self.__photo_name : str = ""
        self.__i = 0
        self.__printer_in_trouble = False
       

    def show(self):
        self.__i = 0
        try:
            self.__printer = TestPrinter()
        except Exception as e:
            self._logger.warning("The printer seems to be not connected, Check if it's turned on and that it's connected correctly")
            self._logger.warning(f"Error : {e}")
            self.__printer_in_trouble = True
        self.__photo_name = self._get_artifact("photo_name")
        self.__timer = time.time()
        self.__printing_text = TextMessage(self._window, "Printing ... ",
                                            center_x=CenterMode.CENTER, font_size=400,
                                            center_y=CenterMode.CENTER, color=FiColor.WHITE)
        
        

    def setup(self):
        self._window.fill(FiColor.SURFACE)
        self.__printing_text.setup()
        if self.__i == 2:
            if not self.__printer_in_trouble:
                self.__print()
        if time.time() - self.__timer > 1: 
            self._go_next_state()
        self.__i+=1
        
        

    def destroy(self):
        if not self.__printer_in_trouble:
            del self.__printer
        pass


    def __print(self):
        try:
            self.__printer.print(self.__photo_name)
        except Exception as e:
            self._logger.warning("Error when printing : This photo could not be printed !")
            self._logger.warning(f"{e}")        