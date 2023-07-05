

class FlashController:
    def __init__(self):
        pass

    def flash_on(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(4, gpio.OUT)
        print("on")
        gpio.output(4, gpio.HIGH)
        time.sleep(0.1)

    def flash_off():
        gpio.setmode(gpio.BCM)
        gpio.setup(4, gpio.OUT)
        print("off")
        gpio.output(4, gpio.LOW)
        time.sleep(1)
