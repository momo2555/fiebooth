import threading
import time

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
            time.sleep(0.02)


