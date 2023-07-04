import RPi.GPIO as gpio
import time
from datetime import datetime
from signal import signal, SIGINT
from sys import exit
import os

gpio.setmode(gpio.BCM)
gpio.setup(26, gpio.IN,pull_up_down=gpio.PUD_UP)

temps_attente=2550
largeur_ecran=2312
hauteur_ecran=1736
largeur_photo=4624
hauteur_photo=3472
resolution=64

#nom_image="photoflashoohoohohon"
pin_btn=26
date_today=datetime.now()
nom_image=date_today.strftime('%d-%m-%Y_%Mm-%Ss')

def prise_photo():
        print("photo lancee")
        flash_on()
        cmd="libcamera-still -t {} --viewfinder-width {} --viewfinder-height {} --width {} --height {} -o {}mp-{}.jpg --autofocus-window 50"
        retour_cmd=os.system(cmd.format(temps_attente,largeur_ecran,hauteur_ecran,largeur_photo,hauteur_photo,resolution,nom_image))
        print(retour_cmd)
        flash_off()
    
def flash_on():
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

while True:
    try:
        print("\n attente boucle")
        #on attend la pression du bouton 
        gpio.wait_for_edge(26,gpio.FALLING)
        #on prend la photo
        prise_photo()
        print("photo enregistrée")
    
    except KeyboardInterrupt:
        print("sorite du programme")
        raise
    
#reinit GPIO lors d'une sorite normale
gpio.cleanup()