### ****************************************************************************************
### *                                                                                      *
### *               CONFIG FILE - ALL CONSTANRS                                            *
### *               FIEBOOTH ~ ALL RIGHTS RESERVED                                         *
### *                                                                                      *
### ****************************************************************************************
import pygame


BP_PIN = 18																			#Pin name for yellow button

MAIN_PATH = "/home/pi/Downloads/FieboothV2"											#main project path
MAIN_LIST = MAIN_PATH + "/*.jpg"													#main picture list
PICTURES_PATH = MAIN_PATH + "/images"												#path for picture folder storage
PICTURES_LIST = PICTURES_PATH + "/*.jpg"											#picutres list
TEMP_PATH = MAIN_PATH + "/temp"														#path for temp folder storage
TEMP_LIST = TEMP_PATH + "/*.jpg"													#temp file list

FILE_INIT = MAIN_PATH + "/" + "FieboothScreen.jpg"									#fond screen for gloal app
FILE_PRINTER = TEMP_PATH + "/" + "last_resized_picture.jpg"							#temp file for fast printing
FILE_SETUP = TEMP_PATH + "/" + "setupCapture.jpg"									#temp file for printer setup
FILE_SETUP_TEMP = TEMP_PATH + "/" + "tempSetupCapture.jpg"							#temp file for brightness and contrast setup

WIDTH_DISPLAY = 1920																#screen size
HEIGHT_DISPLAY = 1080																#screen size

WIDTH_PRINTER = 1280																#image size for printer or 600
HEIGHT_PRINTER = 853																#image size for printer or 309

HEIGHT_TEXT = 300
FONT = None

TIMEOUT = 15																		#printer and camre task time out (in seconds)

SHOW_GALLERY_TIME = 10000															#time (in milliseconds) between each gallery picture
SHOW_PICTURE_TIME = 20000 															#time (in milliseconds) to show you the picture just taken

WHITE = pygame.Color(255,255,255)													#short link for WHITE color
BLACK = pygame.Color(0,0,0)															#short link for BLACK color
BLUE =  pygame.Color(0,0,255)
GREEN =  pygame.Color(0,255,0)
RED =  pygame.Color(255,0,0)
ORANGE =  pygame.Color(255,100,10)
YELLOW =  pygame.Color(255,255,0)


APP_NAME = "Fiebooth V2"
HOME_DELAY = 6

USER_NAME = "guest"
USER_PASSWORD = "123"