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
        self.__buttons : Dict[List] = {}
        self.__lock_buttons : List[int] = []
        self.logger = logging.getLogger("fiebooth")
        self.__thread_safe = Lock()
        self.__use_keyboard = config.use_keyboard
        self.__pressed_lock = None
        self.__lock_timer = time.time()
        self.__pressed_trigger = None
        gpio.setmode(gpio.BCM)

    def add_button(self, trigger, callback, lock=None, key=None):
        #manage trigger button
        self.__pressed_lock = None
        self.__pressed_trigger = None
        
        if not trigger in self.__buttons.keys():
            self.logger.info(f"No trigger registered for t={trigger}")
            self.__buttons[trigger] = []
            gpio.setup(trigger, gpio.IN, pull_up_down=gpio.PUD_UP)
            def button_trigger_rise_cb(e):
                print(e)
                with self.__thread_safe:
                    if self.__pressed_trigger is None:
                        self.__pressed_trigger = trigger
                        print(f"pressed trigger = {self.__pressed_trigger}")
                    #else: 
                    #    self.__pressed_trigger = None
                
            self.logger.info(f"Rise callback  t={trigger}")
            gpio.add_event_detect(trigger, gpio.RISING, callback=button_trigger_rise_cb, bouncetime=300)
            
        
        # manage lock button
        if lock is not None and lock not in self.__lock_buttons:
            self.__lock_buttons.append(lock)
            gpio.setup(lock, gpio.IN, pull_up_down=gpio.PUD_UP)
            def button_lock_rise_cb(e):
                with self.__thread_safe:
                    self.__pressed_lock  = lock
                    self.__lock_timer = time.time()
                print(f"pressed lock = {self.__pressed_lock}")
                self.logger.debug("Pressed lock")
            
            gpio.add_event_detect(lock, gpio.RISING, callback=button_lock_rise_cb, bouncetime=5)

        
        self.__buttons[trigger].append(
            {
                "lock" : lock,
                "key" : key,
                "eventhold" : False,
                "callback" : callback
            }
        )
        

        
        
        

    def setup(self):
        # keyboard event
        if self.__use_keyboard:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.logger.info(f"Button pressed {event.key} with keyboard")
                    for button in self.__buttons:
                        if button["key"] == event.key:
                            button["callback"](None)
        # exec button event
        if self.__pressed_trigger is not None and self.__pressed_trigger in self.__buttons.keys():
            with self.__thread_safe:
                for event in self.__buttons[self.__pressed_trigger]:
                    if (event["lock"] is None and self.__pressed_lock is None) or event["lock"] == self.__pressed_lock:
                        
                        event["callback"](None)
                self.__pressed_trigger = None
                self.__pressed_lock = None
        # unlock after a timeout
        if not self.__pressed_lock is None and time.time() - self.__lock_timer > 4:
            with self.__thread_safe:
                self.__pressed_lock = None


    def __get_button(self, trigger):
        for button in self.__buttons:
            if button["trigger"] == trigger:
                return button
        return None

    def clear_triggers(self):
        for trigger in self.__buttons.keys():
            self.__buttons[trigger] = []
        self.__pressed_lock = None
        self.__pressed_trigger = None
        self.logger.info("Cleanup function is called")
        #gpio.cleanup()