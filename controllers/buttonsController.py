import threading
import time
import pygame

class ButtonsController():
    def __init__(self):
        self.buttons = []
        print("init of buttons controller")
        

    def addButton(self, trigger, callback):
        print("add new button")
        self.buttons.append(
            {
                "trigger" : trigger,
                "callback" : callback
            }
        )
    
    def setup(self):
        print("run button thread")
        while True:
            #if a GPIO is triggered
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    print("button pressed")
                    for button in self.buttons:
                        if button["trigger"] == event.key:
                            button["callback"]()


