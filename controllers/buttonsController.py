import threading
import time
import pygame

class ButtonsController():
    def __init__(self):
        self.buttons = []
        print("init of buttons controller")
        

    def add_button(self, trigger, callback):
        print("add new button")
        self.buttons.append(
            {
                "trigger" : trigger,
                "callback" : callback
            }
        )
    
    def setup(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                print(f"button pressed --- {event.key}")
                for button in self.buttons:
                    if button["trigger"] == event.key:
                        button["callback"]()


