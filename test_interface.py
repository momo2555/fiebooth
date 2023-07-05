from config import config
import pygbutton	
import pygame
import time

screen = pygame.display.set_mode((config.WIDTH_DISPLAY, config.HEIGHT_DISPLAY),pygame.FULLSCREEN) 	#window creation and openning

skip_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-160),50,80,30), "SKIP")   		# Create SKIP button (x, y, x_size, y_size)
quit_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-80),50,80,30), "QUIT")    		# Create QUIT button 
take_pic_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-920),(config.HEIGHT_DISPLAY-200),200,60), "photo")# Create Take Picture button
print_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-690),(config.HEIGHT_DISPLAY-200),200,60), "imprimer")			# Create Print button
contrast_more_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-380),(config.HEIGHT_DISPLAY-440),80,60), "+")		# Create Contrast + button
contrast_less_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-220),(config.HEIGHT_DISPLAY-440),80,60), "-")		# Create Contrast - button
brightness_more_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-380),(config.HEIGHT_DISPLAY-290),80,60), "+")		# Create Brightness + button
brightness_less_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-220),(config.HEIGHT_DISPLAY-290),80,60), "-")		# Create Brightness - button
validate_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-380),(config.HEIGHT_DISPLAY-200),240,60), "VALIDER")		# Create Validate button
yes_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-380),(config.HEIGHT_DISPLAY-190),80,60), "OUI")				# Create YES button
no_button = pygbutton.PygButton(((config.WIDTH_DISPLAY-220),(config.HEIGHT_DISPLAY-190),80,60), "NON")				# Create NO button

#¤v3s
brightness_more_button_small = pygbutton.PygButton(((config.WIDTH_DISPLAY-50),50,20,20), "+")		# Create Brightness + button on main screen 
brightness_less_button_small = pygbutton.PygButton(((config.WIDTH_DISPLAY-50),100,20,20), "-") #on main screen

pygame.init()	#init library
pygame.display.set_caption(config.APP_NAME)

screen = pygame.display.set_mode((config.WIDTH_DISPLAY,config.HEIGHT_DISPLAY),pygame.FULLSCREEN)

while True:
    load = pygame.image.load("accueil.jpg").convert_alpha()
    image = pygame.transform.scale(load,(config.WIDTH_DISPLAY,config.HEIGHT_DISPLAY))
    screen.blit(image,(0,0))
    skip_button.draw(screen)    #print SKIP button
    quit_button.draw(screen)    #print QUIT button 
    time.sleep(0.01)
    pygame.display.update()