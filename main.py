from controllers.buttonsController import ButtonsController
from controllers.cameraController import CameraController

from views.mainWindow import MainWindow
import pygame
import os
import logging

from datetime import datetime

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
    mainWindow = MainWindow()



    while True:
        mainWindow.setup()
        
            

