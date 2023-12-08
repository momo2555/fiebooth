import RPi.GPIO as gpio
import time
import logging
from config import config

class FlashController:

    def __init__(self):
        self.logger = logging.getLogger("fiebooth")
        gpio.setmode(gpio.BCM)
        gpio.setup(config.flash_pin, gpio.OUT)

    def flash_on(self):
        self.logger.info(f"Flash ON")
        gpio.output(4, gpio.HIGH)
        time.sleep(0.1)

    def flash_off(self):
        self.logger.info(f"Flash OFF")
        gpio.output(4, gpio.LOW)

    def clean(self):
        gpio.cleanup()
        
