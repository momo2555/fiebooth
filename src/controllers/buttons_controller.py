import threading
import time
import pygame
import logging
from typing import Dict, Any, List
from config import config
import RPi.GPIO as gpio
from threading import Lock

class ButtonsController():
    def __init__(self):
        self.__buttons : List[Dict[str, Any]] = []
        self.logger = logging.getLogger("fiebooth")
        self.__event_lock = Lock()
        self.__use_keyboard = config.use_keyboard
        gpio.setmode(gpio.BCM)

    def add_button(self, trigger, callback, lock=None, key=None):
        self.__buttons.append(
            {
                "trigger" : trigger,
                "lock" : lock,
                "key" : key,
                "eventhold" : False,
                "callback" : callback
            }
        )
        gpio.setup(trigger, gpio.IN, pull_up_down=gpio.PUD_UP)
        def gpio_callback(e):
            bt = self.__get_button(trigger)
            if (bt is not None):
                with self.__event_lock:
                    bt["eventhold"] = True
        gpio.add_event_detect(trigger, gpio.RISING, callback=gpio_callback, bouncetime=200)

    def setup(self):
        if self.__use_keyboard:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.logger.info(f"Button pressed {event.key} with keyboard")
                    for button in self.__buttons:
                        if button["key"] == event.key:
                            button["callback"](None)
        for button in self.__buttons:
            with self.__event_lock:
                if button["eventhold"]:
                    self.logger.info(f"Physical button pressed")
                    button["callback"](None)
                    button["eventhold"] = False

    def __get_button(self, trigger):
        for button in self.__buttons:
            if button["trigger"] == trigger:
                return button
        return None

    def clear_triggers(self):
        self.__buttons = []
        gpio.cleanup()