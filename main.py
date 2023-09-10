from controllers.buttonsController import ButtonsController
from controllers.cameraController import CameraController
from controllers.test_printer import TestPrinter

from views.main_window import MainWindow
import pygame
import os
import logging

from datetime import datetime
from api.api import FieboothApi


def __init_logger():
    logger = logging.getLogger('fiebooth')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


if __name__ == "__main__":
    __init_logger()
    api = FieboothApi()
    #mainWindow = MainWindow()
    api.run_server()



    while True:
        pass
    #    try:
    #        mainWindow.setup()
    #    except KeyboardInterrupt as e:
    #        logging.getLogger("fiebooth").info(f"User Exit - Keyboard interrupt")
    #        exit(0)

