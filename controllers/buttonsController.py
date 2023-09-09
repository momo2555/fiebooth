import threading
import time
import pygame
import logging
from typing import Dict, Any, List

class ButtonsController():
    def __init__(self):
        self.__buttons : List[Dict[str, Any]] = []
        self.logger = logging.getLogger("fiebooth")
        
        

    def add_button(self, trigger, callback):
        self.__buttons.append(
            {
                "trigger" : trigger,
                "callback" : callback
            }
        )
    
    def setup(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.logger.info(f"Button pressed {event.key}")
                for button in self.__buttons:
                    if button["trigger"] == event.key:
                        button["callback"]()


    def clear_triggers(self):
        self.__buttons = []