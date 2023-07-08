from controllers.buttonsController import ButtonsController
from views.mainWindow import MainWindow
import pygame

def test():
    print("AAAAAAAAAAAAAAAAAAAAAA")

if __name__ == "__main__":
    mainWindow = MainWindow()

    buttonsController = ButtonsController()
    buttonsController.addButton(pygame.K_a, test)
    

    

    while True:
        #buttonsController.setup()
        mainWindow.setup()

