from controllers.buttons_controller import ButtonsController
from controllers.cameraController import CameraController
from controllers.test_printer import TestPrinter

from views.main_window import MainWindow
import pygame
import os
import logging

from multiprocessing import Pipe
from datetime import datetime
from api.api import FieboothApi
from config import env


def __init_logger():
    logger = logging.getLogger('fiebooth')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] : %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info(f"LOAD MESSAGE: {env.LOAD_MESSAGE}")


if __name__ == "__main__":
    api_conn, pyg_conn = Pipe()
    __init_logger()
    mainWindow = MainWindow(pyg_conn)
    api = FieboothApi(api_conn)
    api.run_server()
    while True:
        try:
            mainWindow.setup()
            pass
        except KeyboardInterrupt as e:
            logging.getLogger("fiebooth").info(f"User Exit - Keyboard interrupt")
            exit(0)

    
