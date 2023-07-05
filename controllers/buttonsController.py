import threading
import time
import pygame

class ButtonsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.buttons = []
        print("init of buttons controller")
        

    def addButton(self, trigger, callback):
        self.buttons.append(
            {
                "trigger" : trigger,
                "callback" : callback
            }
        )
    
    def run(self):
        while True:
            #if a GPIO is triggered
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    for button in self.buttons:
                        if button["trigger"] == event.key:
                            button["callback"]()
                            
            time.sleep(0.02)


