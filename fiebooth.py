# EXECUTE THIS FILE LIKE THIS:
# > sudo python FILENAME.py

#need folder "images" (where pictures will be store) and "temp" (for temporary picture tranformations)
#need file "FieboothScreen.jpg" for first screen display

import os
import os.path
import subprocess as sub
import sys
import shutil
import usb.core
#import shlex
import datetime
import time
import pygbutton																	#pygame button library
import glob																			#path folder navigation library
import sys
import pygooey																		#textbox library
import pygame																		#display library
import cups																			#serial printer communication library
from threading import Thread
import RPi.GPIO as GPIO
#from wifi import Cell, Scheme
import gphoto2 as gp																#camera library
from time import sleep
from pygame.locals import *
from PIL import Image, ImageEnhance 												#image convertion library

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

WIDTH_DISPLAY = 1024																#screen size
HEIGHT_DISPLAY = 600																#screen size

WIDTH_PRINTER = 1280																#image size for printer or 600
HEIGHT_PRINTER = 853																#image size for printer or 309

HEIGHT_TEXT = 300
FONT = None

TIMEOUT = 15																		#printer and camre task time out (in seconds)

SHOW_GALLERY_TIME = 10000															#time (in milliseconds) between each gallery picture
SHOW_PICTURE_TIME = 20000 															#time (in milliseconds) to show you the picture just taken

app_status = True																	#False when catching exception that need to close the app
loop_init = True																	#for continuous execution in INIT APP
loop_wifiConnection = False
loop_eventName = False																#for continuous execution in INIT APP
loop_printerSetUp = False															#for continuous execution in PRINTER SET UP APP
loop_gallery_setup = False															#for continuous execution in GALLERY SETUP APP
loop_gallery = False																#for continuous execution in GALLERY APP

in_process = False																	#exclusive variable for tasks
camera_available = False															#variable for camera init
printer_available = False															#variable for printer init

camera = gp.Camera()

waiting_on_download = False 														#if this is true, look for last_image_taken
waiting_on_print = False															#if this is true, waiting picture print

screen = pygame.display.set_mode((WIDTH_DISPLAY,HEIGHT_DISPLAY),pygame.FULLSCREEN) 	#window creation and openning

skip_button = pygbutton.PygButton(((WIDTH_DISPLAY-160),50,80,30), "SKIP")   		# Create SKIP button (x, y, x_size, y_size)
quit_button = pygbutton.PygButton(((WIDTH_DISPLAY-80),50,80,30), "QUIT")    		# Create QUIT button 
take_pic_button = pygbutton.PygButton(((WIDTH_DISPLAY-920),(HEIGHT_DISPLAY-200),200,60), "photo")# Create Take Picture button
print_button = pygbutton.PygButton(((WIDTH_DISPLAY-690),(HEIGHT_DISPLAY-200),200,60), "imprimer")			# Create Print button
contrast_more_button = pygbutton.PygButton(((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-440),80,60), "+")		# Create Contrast + button
contrast_less_button = pygbutton.PygButton(((WIDTH_DISPLAY-220),(HEIGHT_DISPLAY-440),80,60), "-")		# Create Contrast - button
brightness_more_button = pygbutton.PygButton(((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-290),80,60), "+")		# Create Brightness + button
brightness_less_button = pygbutton.PygButton(((WIDTH_DISPLAY-220),(HEIGHT_DISPLAY-290),80,60), "-")		# Create Brightness - button
validate_button = pygbutton.PygButton(((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-200),240,60), "VALIDER")		# Create Validate button
yes_button = pygbutton.PygButton(((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-190),80,60), "OUI")				# Create YES button
no_button = pygbutton.PygButton(((WIDTH_DISPLAY-220),(HEIGHT_DISPLAY-190),80,60), "NON")				# Create NO button

#¤v3s
brightness_more_button_small = pygbutton.PygButton(((WIDTH_DISPLAY-50),50,20,20), "+")		# Create Brightness + button on main screen 
brightness_less_button_small = pygbutton.PygButton(((WIDTH_DISPLAY-50),100,20,20), "-") #on main screen

WHITE = pygame.Color(255,255,255)													#short link for WHITE color
BLACK = pygame.Color(0,0,0)															#short link for BLACK color
BLUE =  pygame.Color(0,0,255)
GREEN =  pygame.Color(0,255,0)
RED =  pygame.Color(255,0,0)
ORANGE =  pygame.Color(255,100,10)
YELLOW =  pygame.Color(255,255,0)

contrast_value = 1.0																#value for printer contrast
brightness_value = 1.0																#value for printer brightness

image_name = ""																		#to share image in Load functions
image_name_taken = ""																#save image name just taken
delay_time = .005																	#delay time for main loop
last_image_taken = ""																#to save last image taken

current_image = 0																	#index for object_list
image_count = 0
object_list = [] 																	#list of preloaded images
change_ticks = 0
last_image_number = 0

#***************THREAD****************************************************************************

class PrinterThread(Thread):
	
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		init_time = time.clock()
		current_time = init_time
		#print("Initial time : ", init_time)
		printer_status = "IDLE"
		
		#file1 = open("printerLogs.txt","a")

		while current_time < (init_time + float(TIMEOUT)) and printer_status != "PRINTING COMPLET":
			current_time = time.clock()
			conn = cups.Connection()
			printers = conn.getPrinters()
			for printer in printers:
				printers_message = str(printers[printer]["printer-state-message"])
				printers_state = str(printers[printer]["printer-state"])
			jobs_message = str(conn.getJobs(requested_attributes=["job-id",'job-state-reasons']))
			jobs_state = str(conn.getJobs(requested_attributes=["job-id",'job-state']))
			cut_jobs_message = jobs_message
			cut_jobs_state = jobs_state

			if cut_jobs_state != "{}":	#jobState way of save value
				for r in (("{", ""), (" ",""), ("}", "")):
					cut_jobs_state = cut_jobs_state.replace(*r)
				cut_jobs_state = cut_jobs_state.split(":")
				jobs_state = cut_jobs_state[2]
			else:
				jobs_state = ""
			if cut_jobs_message != "{}":	#jobMessage way of save value
				for r in (("{", ""), (" ",""), ("}", ""), ("u'", ""), ("'", "")):
					cut_jobs_message = cut_jobs_message.replace(*r)
				cut_jobs_message = cut_jobs_message.split(":")
				jobs_message= cut_jobs_message[2]
			else:
				jobs_message = ""

			#file1.write(printers_message + ";" + printers_state + ";")
			#file1.write(jobs_message + ";" + jobs_state + "\n")

			if printers_message == "" and printers_state == "3" and jobs_message == "" and jobs_state == "":
				printer_status = "IDLE"
			elif printers_message == "" and printers_state == "3" and jobs_message == "job-incoming" and jobs_state == "4":
				printer_status = "JOB INCOMING"
			elif printers_message == "" and printers_state == "3" and jobs_message == "job-incoming" and jobs_state == "5":
				printer_status = "JOB INCOMING - TRANSITION"
			elif printers_message == "" and printers_state == "3" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "JOB PRINTING - TRANSITION"
			elif printers_message == "" and printers_state == "4" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "JOB PRINTING - TRANSITION PRINTER"
			elif printers_message == "Sending data to printer." and printers_state == "4" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "JOB PRINTING - SENDING DATA"
			elif "last_resized_picture.jpg" in printers_message and printers_state == "4" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "JOB PRINTING"
			elif "Printing Page" in printers_message and printers_state == "4" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "JOB PRINTING - IN PROGRESS"
			elif printers_message == "The printer is ready to print." and printers_state == "4" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "PRINTING COMPLET"
			elif printers_message == "Waiting for printer to become available." and printers_state == "4" and jobs_message == "job-printing" and jobs_state == "5":
				printer_status = "ISSUE - SENDING DATA"
			else :
				printer_status = "UNKNOW "
				print(printers_message, printers_state, jobs_message, jobs_state)

			print("init time = ", init_time)
			print("time is : ", current_time)
			print("printer status is : ", printer_status)

		print("Finish time : ", current_time)
		#file1.close()

#***************FUNCTIONS****************************************************************************

def RenderOverlay(application_name):
#DEBUG#    print("START of RenderOverlay")
	if application_name == "Fiebooth V2_GALLERY":
		#app name
		#screen.blit(pygame.font.SysFont("freeserif",30,bold=0).render(application_name, 1, WHITE),((WIDTH_DISPLAY-350),10))
		#button
		quit_button.draw(screen)
		#¤v3
		brightness_more_button_small.draw(screen)
		brightness_less_button_small.draw(screen)

		pygame.display.update()
	elif application_name == "Fiebooth V2_PRINTER SET UP APP":
		#app name
		LoadImageObjectToScreen(object_list[0])	
		#screen.blit(pygame.font.SysFont("freeserif",30,bold=0).render(application_name, 1, WHITE),((WIDTH_DISPLAY-350),10))
		pygame.draw.rect(screen, BLACK, (100,100,440,293),0) 				#x position, y position, weight, HEIGHT_DISPLAY
		DrawMessage("Wait...",400,70,100,100,40,BLACK)
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-500),240,60),0) 				#WHITE rectangle for contrast title
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-350),240,60),0) 				#WHITE rectangle for brightness title
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-440),80,60),0) 				#WHITE rectangle for contrast value
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-290),80,60),0) 				#WHITE rectangle for brightness value
		screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("CONTRASTE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-500))
		screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("LUMINOSITE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-350))
		screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(contrast_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-440))
		screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(brightness_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-290))
		print_button.draw(screen)
		contrast_more_button.draw(screen)
		contrast_less_button.draw(screen)
		brightness_more_button.draw(screen)
		brightness_less_button.draw(screen)
		take_pic_button.draw(screen)
		validate_button.draw(screen)
		skip_button.draw(screen)    #print SKIP button
		quit_button.draw(screen)    #print QUIT button 

		pygame.display.update()
#DEBUG#    print("END of RenderOverlay")

def LoadImageToObjectList(image_name):
#DEBUG#	print("START of LoadImageToObjectList")
	#load image by filename to the list of image objects for fast switching
	global object_list
	global image_count
	global last_image_number
	
#DEBUG#	print ("LoadImageToObjectList: " + image_name)
#DEBUG#	print ("before load: " + str(pygame.time.get_ticks()))
	load = pygame.image.load(image_name).convert_alpha()
#DEBUG#	print ("loaded: " + str(pygame.time.get_ticks()))
	scale = pygame.transform.scale(load,(WIDTH_DISPLAY,HEIGHT_DISPLAY))
#DEBUG#	print ("scaled: " + str(pygame.time.get_ticks()))
#DEBUG#	print ("before append")
	object_list.append(scale)
	last_image_number = image_count    
	image_count = image_count + 1
#DEBUG#	print ("after append" + str(pygame.time.get_ticks()))
#DEBUG#	print ("added to object_list: " + str(len(object_list)))	
	pygame.display.update()
#DEBUG#	print("END of LoadImageToObjectList")

def LoadImageObjectToScreen(image):
#DEBUG#    print("START of LoadImageObjectToScreen")
	#load the image object from the list to the screen
#DEBUG#    print ("before load: " + str(pygame.time.get_ticks()))
	screen.blit(image,(0,0))
#DEBUG#    print ("added to screen: " + str(pygame.time.get_ticks()))
	pygame.display.update()   	
#DEBUG#    print ("END LoadImageObjectToScreen")

def NextPicture():
#DEBUG#    print("START of NextPicture")
	#draws the prev picture in the list from the object list
	global current_image
	global in_process
	if not in_process:
		in_process = True
		current_image = current_image + 1
		if current_image > (len(object_list)-1):
			current_image = 0
		in_process = False
#DEBUG#    print ("END NextPicture")    

def GetDateTimeString():
#DEBUG#    print("START of GetDateTimeString")
	#format the datetime for the time-stamped filename
	dt = str(datetime.datetime.now()).split(".")[0]
	clean = dt.replace(" ","").replace(":","")
	return clean
#DEBUG#    print("END of GetDateTimeString")

def DrawMessage(message,WIDTH_DISPLAY,HEIGHT_DISPLAY,x,y,size,Bcolor):
#DEBUG#    print("START of DrawMessage")
	#displays notification messages onto the screen

	backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))#size
	backgroundCenterSurface.fill(Bcolor)

	screen.blit(backgroundCenterSurface,(x,y))#position
	screen.blit(pygame.font.SysFont("freeserif",size,bold=1).render(message, 1, WHITE),(x+10,y+10))
	pygame.display.update()
#DEBUG#    print("END of DrawMessage")

def LoadNewImage():
#DEBUG#    print("START of LoadNewImage")
	# after new image has been downloaded from the camera
	# it must be loaded into the object list and displayed on the screen
	global waiting_on_download
	global waiting_on_print
	global image_count
	global last_image_number
	global current_image

	DrawMessage("DOWNLOADING PICTURE",200,20,0,0,10,BLACK)

#DEBUG#    print ("start LoadNewImage: " + str(pygame.time.get_ticks()))
	capture = pygame.transform.scale(pygame.image.load(last_image_taken).convert_alpha(),(WIDTH_DISPLAY,HEIGHT_DISPLAY))
	#capture = pygame.transform.rotate(capture, 180) 							#<----------------------------------ROTATION
#DEBUG#    print ("capture transformed: " + str(pygame.time.get_ticks()))

	DrawMessage("LOADING IMAGE",200,20,0,0,10,BLACK)

	screen.blit(capture,(0,0))
	object_list.append(capture)

	last_image_number = image_count
	current_image = last_image_number
	image_count = image_count + 1
#DEBUG#    print ("capture added to screen: " + str(pygame.time.get_ticks()))    
	waiting_on_download = False
	waiting_on_print = True
#DEBUG#    print("END of LoadNewImage")   

def OpenBasicWindow(name):
	DrawMessage("WAIT...",700,70,20,390,40,BLACK)
	LoadImageObjectToScreen(object_list[0])	
	#screen.blit(pygame.font.SysFont("freeserif",30,bold=0).render(name, 1, WHITE),((WIDTH_DISPLAY-350),10))

	skip_button.draw(screen)    #print SKIP button
	quit_button.draw(screen)    #print QUIT button 
	pygame.display.update()

def SmileTimer():
	pygame.draw.rect(screen, BLACK, (0,0,WIDTH_DISPLAY,HEIGHT_DISPLAY),0) 				#x position, y position, weight, HEIGHT_DISPLAY
	init_time = time.clock()
	current_time = init_time
	while current_time <= (init_time + float(4)):
		if current_time <= init_time + float(1):
			backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))#size
			backgroundCenterSurface.fill(BLACK)
			screen.blit(backgroundCenterSurface,(0,0))#position
			font = pygame.font.Font(FONT, HEIGHT_TEXT)	#font type , text size
			text = font.render('3', True, WHITE, None) 					#'text', antialias , text color, background color
			textRect = text.get_rect() 
			textRect.center = (WIDTH_DISPLAY // 2 , HEIGHT_DISPLAY // 2) 
			screen.blit(text, textRect)
		elif current_time <= init_time + float(2) and current_time > init_time + float(1):
			backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))#size
			backgroundCenterSurface.fill(BLACK)
			screen.blit(backgroundCenterSurface,(0,0))#position				
			font = pygame.font.Font(FONT, HEIGHT_TEXT)	#font type , text size
			text = font.render('2', True, WHITE, None) 					#'text', antialias , text color, background color
			textRect = text.get_rect() 
			textRect.center = (WIDTH_DISPLAY // 2 , HEIGHT_DISPLAY // 2) 
			screen.blit(text, textRect)
		elif current_time <= init_time + float(3) and current_time > init_time + float(2):
			backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))#size
			backgroundCenterSurface.fill(BLACK)
			screen.blit(backgroundCenterSurface,(0,0))#position				
			font = pygame.font.Font(FONT, HEIGHT_TEXT)	#font type , text size
			text = font.render('1', True, WHITE, None) 					#'text', antialias , text color, background color
			textRect = text.get_rect() 
			textRect.center = (WIDTH_DISPLAY // 2 , HEIGHT_DISPLAY // 2) 
			screen.blit(text, textRect)
		elif current_time <= init_time + float(4) and current_time > init_time + float(3):
			backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))#size
			backgroundCenterSurface.fill(BLACK)
			screen.blit(backgroundCenterSurface,(0,0))#position			
			font = pygame.font.Font(FONT, HEIGHT_TEXT)	#font type , text size
			text = font.render('SMILE :)', True, WHITE, None) 					#'text', antialias , text color, background color
			textRect = text.get_rect() 
			textRect.center = (WIDTH_DISPLAY // 2 , HEIGHT_DISPLAY // 2) 
			screen.blit(text, textRect)
		else:
			backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))#size
			backgroundCenterSurface.fill(BLACK)
			screen.blit(backgroundCenterSurface,(0,0))#position			
			DrawMessage("TIME ISSUE !!!",400,70,(0,0),40,RED)
		pygame.display.update()
		current_time = time.clock()
	#return to saved context

def PrintPicture():
#DEBUG#    print("START of PrintPicture")
	# executes the lp (cups) command to print the current image
	global print_command
	global waiting_on_print
	global image_name_taken
	
	resize_img = pygame.transform.scale(pygame.image.load(PICTURES_PATH + "/" + image_name_taken), (WIDTH_PRINTER, HEIGHT_PRINTER))
	pygame.image.save(resize_img,FILE_PRINTER)

	GreyPictureSetUp(FILE_PRINTER, FILE_PRINTER)
	
	print_command = "lp -d Brother_QL-800 " + FILE_PRINTER
	#executes command below
	try:
		p = sub.Popen(print_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
		#thread_1.start()
		DrawMessage("impression en cours",200,20,0,0,10,BLACK)
	except:
		DrawMessage("probleme impression",200,20,0,0,10,RED)

	waiting_on_print = False
#DEBUG#    print("END of PrintPicture")   

def InitCamera():
	global camera
	try:
		camera = gp.Camera()
		camera.init()
		return (True, "")
	except gp.GPhoto2Error as ex:
		if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
		# no camera
			return (False, "Camera disconnected")
		else:
		# some other error we can't handle here
			print(gp.GPhoto2Error(ex.code))
			return (False, "Camera issue : " + gp.GPhoto2Error(ex.code))

def TakePicture(application_name, path_name):
#DEBUG#    print("START of TakePicture")
	# executes the gphoto2 command to take a photo and download it from the camera
	global last_image_taken
	global waiting_on_download
	global image_name_taken
	global camera
	check = False

	camera_state = InitCamera()
	file_list = glob.glob(path_name + "/*.jpg")
	
	if camera_state[0] == True:
		image_name_taken = "capture" + GetDateTimeString() + ".jpg"

		if application_name == "Fiebooth V2_GALLERY":
			last_image_taken = PICTURES_PATH + "/" + image_name_taken

		cpt_image_name_taken = path_name + "/" + image_name_taken
		#take_pic_command = "gphoto2 --capture-image-and-download --filename=" + last_image_taken + " --force-overwrite"
		try:
			#p = sub.Popen(take_pic_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
			i2 = camera.capture(gp.GP_CAPTURE_IMAGE)
			check = True
		except gp.GPhoto2Error as ex:
			DrawMessage("Vous êtes peut-être trop près de l'appareil photo : reculez ! ",700,70,0,0,40,BLACK)
			sleep(6)
		if check:
			try:
				init_time = time.clock()
				current_time = init_time
				f2 = camera.file_get(i2.folder,i2.name,gp.GP_FILE_TYPE_NORMAL)
				dest2 = os.path.join(path_name,image_name_taken)
				# try:
				# 	shutil.copy(source, dest2)
				# except IOError as e:
				# 	print("Unable to copy file. %s" % e)
				# except:
				# 	print("Unexpected error:", sys.exc_info())
				f2.save(dest2)
				
				# typ,data = camera.wait_for_event(200) #empty the event queue
				# while waiting_on_download == False or typ != gp.GP_EVENT_TIMEOUT:					
				# 	if typ == gp.GP_EVENT_FILE_ADDED:
				# 		DrawMessage("Download picture from Camera OK",700,70,0,0,40,GREEN)
				# 		sleep(6)
				# 		waiting_on_download = True
				# 	elif typ == gp.GP_EVENT_TIMEOUT:
				# 		DrawMessage("Camera busy. Please retry in few seconds",700,70,0,0,40,RED)
				# 		sleep(6)		
				# 	#try to grab another event
				# 	typ,data = camera.wait_for_event(1)
				
				while current_time < (init_time + float(TIMEOUT)) and waiting_on_download == False:	#empty the event queue
					current_time = time.clock()
					file_list = glob.glob(path_name + "/*.jpg")
					if cpt_image_name_taken in file_list:
						waiting_on_download = True
						#DrawMessage("Download picture from Camera OK",700,70,((WIDTH_DISPLAY/2)-220),((HEIGHT_DISPLAY/2)-2),40)
					else:
						DrawMessage("Download picture from Camera issue",700,70,0,0,40,RED)
						sleep(6)
				if current_time >= (init_time + float(TIMEOUT)) and waiting_on_download == False:
					DrawMessage("Camera busy. Please retry in few seconds",700,70,0,0,40,RED)
					sleep(6)
			except:
				DrawMessage("Download picture from Camera issue",700,70,0,0,40,RED)
				sleep(6)
	else:
		DrawMessage(camera_state[1],700,70,0,0,40,RED)
		sleep(6)
	camera.exit()
#DEBUG#    print("END of TakePicture")

def GreyPictureSetUp(file_input, file_output):
#DEBUG#    print("START of GreyPictureSetUp")
	# modify contrast and brightness picture and display
	im = Image.open(file_input)
	enhancer = ImageEnhance.Contrast(im)
	enhancer_im = enhancer.enhance(contrast_value)
	enhancer = ImageEnhance.Brightness(enhancer_im)
	enhancer_im = enhancer.enhance(brightness_value)
	enhancer_im.save(file_output)
#DEBUG#    print("END of GreyPictureSetUp")

def ConvertPictureForDisplay(screen, image_input):
#DEBUG#    print("START of GreyPictureSetUp")
	# modify picture size for display and refresh contrast and brightness values
	load = pygame.image.load(image_input).convert_alpha()
	scale = pygame.transform.scale(load,(440,293)) #scale for preview in rectangle (original scale at 3:2 (4272 x 2848))
	screen.blit(scale,(100,100))
	pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-440),80,60),0) 				#WHITE rectangle for contrast value
	pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-290),80,60),0) 				#WHITE rectangle for brightness value
	screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(contrast_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-440))
	screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(brightness_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-290))
#DEBUG#    print("END of GreyPictureSetUp")

def print_on_enter(id, final):
    print('enter pressed, textbox contains {}'.format(final))
	
#see all settings help(pygooey.TextBox.__init__)
settings = {
	"command" : print_on_enter,
	"inactive_on_enter" : False,
}

def event_text(event_type):
	if event_type == gp.GP_EVENT_CAPTURE_COMPLETE: return "Capture Complete"
	elif event_type == gp.GP_EVENT_FILE_ADDED: return "File Added"
	elif event_type == gp.GP_EVENT_FOLDER_ADDED: return "Folder Added"
	elif event_type == gp.GP_EVENT_TIMEOUT: return "Timeout"
	else: return "Unknown Event"

#***************END FUNCTIONS******************

#***************APPLICATION START****************************************************************************

os.system("sudo pkill gvfs")
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

# try:
# 	clean_memory_command = "sudo tee /var/log/syslog </dev/null"
# 	p = sub.Popen(clean_memory_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
# except:
# 	print ("FAILED to clean syslog")

# try:
# 	clean_memory_command = "sudo rm /var/log/kern*"
# 	p = sub.Popen(clean_memory_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
# except:
# 	print ("FAILED to clean kern")

# try:
# 	clean_memory_command = "sudo rm /var/log/messages*"
# 	p = sub.Popen(clean_memory_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
# except:
# 	print ("FAILED to clean messages")

# try:
# 	clean_memory_command = "trash-empty*"
# 	p = sub.Popen(clean_memory_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
# except:
# 	print ("FAILED to clean trash")

print_command = "cancel -a"  											#Cancel all printer jobs
p = sub.Popen(print_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True) #COMMAND LINE cancel all printer jobs
files = glob.glob(TEMP_PATH + "/*")
for f in files:															#remove */temp/ files
	os.remove(f)

app_name = "Fiebooth V2_INIT"

sleep(2)

pygame.init()	#init library
pygame.display.set_caption(app_name)

screen = pygame.display.set_mode((WIDTH_DISPLAY,HEIGHT_DISPLAY),pygame.FULLSCREEN)#window creation and openning

GPIO.setmode(GPIO.BCM)										#chip reference mode
GPIO.setup(BP_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)		#Enable pull up

while (app_status):

#LOOP INIT------------------------------------------------------------------------------------------------------------------------------------------------
	if loop_init:
		app_name = "Fiebooth V2_INIT"
		try:
			file_list = glob.glob(MAIN_LIST)
		#DEBUG#		print ("files in folder: " + str(len(file_list)))
		except:
		#DEBUG#	print("path folder issue")
			DrawMessage("STORAGE PATH ISSUE",700,70,0,0,40,RED)
			app_status = False

		DrawMessage("WAIT...",700,70,20,390,40,BLACK)

		if FILE_INIT in file_list:				#find pictures and add it in object list
			LoadImageToObjectList(FILE_INIT)
			LoadImageObjectToScreen(object_list[0])	
			#screen.blit(pygame.font.SysFont("freeserif",30,bold=0).render(app_name, 1, WHITE),((WIDTH_DISPLAY-350),10))
		
		OpenBasicWindow(app_name)

		while camera_available == False or printer_available == False:
			dev = usb.core.find(idVendor=0x4f9)
			if dev is None:
				printer_available = False
				DrawMessage("pb imprimante: debranchez 30 secondes",700,70,0,0,40,RED)
			else :
				printer_available = True
				DrawMessage("imprimante connectée",700,70,0,0,40,GREEN)

			dev = usb.core.find(idVendor=0x4a9)
			if dev is None:
				camera_available = False
				DrawMessage("NO CAMERA",700,70,0,200,40,RED)
			else :
				camera_available = True
				DrawMessage("CAMERA CONNECTED",700,70,0,200,40,GREEN)

		loop_init = False
		#loop_wifiConnection = True
		loop_printerSetUp = True	

#LOOP WIFI CONNECTION-------------------------------------------------------------------------------------------------------------------------------------------
	if loop_wifiConnection:
		app_name = "Fiebooth V2_WIFI-CONNECTION"
		OpenBasicWindow(app_name)
		refresh_button = pygbutton.PygButton(((WIDTH_DISPLAY-240),50,80,30), "WIFI")
		connect_button = pygbutton.PygButton(((WIDTH_DISPLAY-320),50,80,30), "CONN")
		refresh_button.draw(screen)
		connect_button.draw(screen)
		pygame.display.update()

		#Loop for Wifi connection
		while(loop_wifiConnection):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop_wifiConnection = False
					app_status = False
				if 'click' in refresh_button.handleEvent(event):
					#"cells = Cell.all('wlan0')
					#print(Cell.all('wlan0'))
					print("refresh")
					#for cell in cells:
						#cell.summary = 'SSID {} / Qual {}'.format(cell.ssid, cell.quality)
						#print(cell.summary)
						#DrawMessage(str(cell.summary),700,70,20,390,40)
				if 'click' in connect_button.handleEvent(event):
					try:
						#cell = Cell.all('wlan0')[2]
						#scheme = Scheme.for_cell('wlan0', 'Oui..', cell, '88888888')
						#scheme.save()
						#scheme.activate()
						print("connect")
					except:
						print("FAILED TO CONNECT")
						loop_wifiConnection = False
						app_status = False
				if 'click' in quit_button.handleEvent(event):
					loop_wifiConnection = False
					app_status = False
				if 'click' in skip_button.handleEvent(event):
					DrawMessage("WAIT...",700,70,20,390,40,BLACK)
					loop_wifiConnection = False
					loop_eventName = True
				pygame.display.update()
				pygame.event.clear()			#remove all other clic in the queue.
#LOOP EVENT NAME-------------------------------------------------------------------------------------------------------------------------------------------
	if loop_eventName:
		app_name = "Fiebooth V2_EVENT-NAME"
		#OpenBasicWindow(app_name)
		#screen = pygame.display.set_mode((WIDTH_DISPLAY,HEIGHT_DISPLAY),pygame.FULLSCREEN)
		try:
			file_list = glob.glob(MAIN_LIST)
		#DEBUG#		print ("files in folder: " + str(len(file_list)))
		except:
		#DEBUG#	print("path folder issue")
			DrawMessage("STORAGE PATH ISSUE",700,70,20,390,40,RED)
			app_status = False

		DrawMessage("WAIT...",700,70,20,390,40,BLACK)

		if FILE_INIT in file_list:				#find pictures and add it in object list
			LoadImageObjectToScreen(object_list[0])	
			#screen.blit(pygame.font.SysFont("freeserif",30,bold=0).render(app_name, 1, WHITE),((WIDTH_DISPLAY-350),10))

		skip_button.draw(screen)    #print SKIP button
		quit_button.draw(screen)    #print QUIT button 
		pygame.display.update()
				
		screen_rect = screen.get_rect()
		pygame.draw.rect(screen, BLACK, (200,100,440,270),0) 				#x position, y position, weight, HEIGHT_DISPLAY						
		DrawMessage("Event Name",400,70,200,100,40,BLACK)
		entry = pygooey.TextBox(rect=(220,300,400,50), **settings)			# Create textbox object  rect=(x position,y position, length, HEIGHT_DISPLAY)
		entry.update()
		entry.draw(screen)	
		pygame.display.update()		#display update
		
		#Loop for Event name capture or Skip
		while(loop_eventName):			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
		#DEBUG#			print ("quiting...")
					loop_eventName = False
					app_status = False
				if 'click' in quit_button.handleEvent(event):
		#DEBUG#                print ("quiting...")
					loop_eventName = False
					app_status = False
				if 'click' in skip_button.handleEvent(event):
					DrawMessage("WAIT...",700,70,20,390,40,BLACK)
					loop_eventName = False
					loop_printerSetUp = True
				entry.get_event(event)
				entry.update()
				entry.draw(screen)				
				pygame.display.update()	
				pygame.event.clear()			#remove all other clic in the queue.
				
#LOOP PRINTER SET UP-------------------------------------------------------------------------------------------------------------------------------------------
	if loop_printerSetUp:
		app_name = "Fiebooth V2_PRINTER SET UP APP"
		OpenBasicWindow(app_name)
		DrawMessage("Prenez une photo et reglez la luminosite puis le contraste.",WIDTH_DISPLAY,(HEIGHT_DISPLAY-(HEIGHT_DISPLAY-100)),0,(HEIGHT_DISPLAY-100),25,BLACK)#(message,WIDTH_DISPLAY,HEIGHT_DISPLAY,x,y,size)

		pygame.draw.rect(screen, BLACK, (100,100,440,293),0) 			#x position, y position, weight, HEIGHT_DISPLAY
		DrawMessage("Prenez une photo",400,70,100,100,40,BLACK)						#(message,WIDTH_DISPLAY,HEIGHT_DISPLAY,x,y)

		print_button.draw(screen)
		contrast_more_button.draw(screen)
		contrast_less_button.draw(screen)
		brightness_more_button.draw(screen)
		brightness_less_button.draw(screen)
		take_pic_button.draw(screen)
		validate_button.draw(screen)
		
		backgroundCenterSurface = pygame.Surface((WIDTH_DISPLAY,HEIGHT_DISPLAY))
		backgroundCenterSurface.fill(BLACK)

		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-500),240,60),0) 				#WHITE rectangle for contrast title
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-350),240,60),0) 				#WHITE rectangle for brightness title
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-440),80,60),0) 				#WHITE rectangle for contrast value
		pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-290),80,60),0) 				#WHITE rectangle for brightness value
		screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("CONTRASTE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-500))
		screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("LUMINOSITE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-350))
		screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(contrast_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-440))
		screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(brightness_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-290))
		pygame.display.update()

		file_list = glob.glob(TEMP_LIST)
		
		#Loop for printer set up
		while(loop_printerSetUp):

			if waiting_on_download and os.path.isfile(TEMP_PATH + "/" + image_name_taken):
				#PRINT picture in rect
				img = Image.open(TEMP_PATH + "/" + image_name_taken).convert('L') #convert in grayscale
				img.save(FILE_SETUP)
				load = pygame.image.load(FILE_SETUP).convert_alpha()
				scale = pygame.transform.scale(load,(440,293)) #scale for preview in rectangle (original scale at 3:2 (4272 x 2848))
				screen.blit(scale,(100,100))

				file_list = glob.glob(TEMP_LIST)
				if FILE_SETUP in file_list:
					resize_img = pygame.transform.scale(pygame.image.load(FILE_SETUP), (WIDTH_PRINTER,HEIGHT_PRINTER))
					pygame.image.save(resize_img,FILE_PRINTER)
					try:
						print_command = "lp -d Brother_QL-800 " + FILE_PRINTER
						p = sub.Popen(print_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
						DrawMessage("print in progress",400,70,100,100,40,BLACK)
					except:
						print("issue in printing")						
				else:
					DrawMessage("print picture issue",400,70,100,100,40,RED)
				waiting_on_download = False
			
				pygame.display.update()
				sleep(2)
				screen.blit(scale,(100,100))
				pygame.display.update()
			
			if GPIO.input(BP_PIN) == 0:
				sleep(0.05)						#debounce time (in seconds)
				if GPIO.input(BP_PIN) == 0:
					SmileTimer()
					TakePicture(app_name, TEMP_PATH)
					RenderOverlay(app_name)
					contrast_value = 1.0
					brightness_value = 1.0
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-500),240,60),0) 				#WHITE rectangle for contrast title
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-350),240,60),0) 				#WHITE rectangle for brightness title
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-440),80,60),0) 				#WHITE rectangle for contrast value
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-290),80,60),0) 				#WHITE rectangle for brightness value
					screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("CONTRASTE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-500))
					screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("LUMINOSITE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-350))
					screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(contrast_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-440))
					screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(brightness_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-290))
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop_printerSetUp = False
					app_status = False
				
				if 'click' in quit_button.handleEvent(event):
					loop_printerSetUp = False
					app_status = False
				
				if 'click' in skip_button.handleEvent(event):
					DrawMessage("WAIT...",400,70,100,100,40,BLACK)
					loop_printerSetUp = False
					loop_gallery = True
				
				if 'click' in validate_button.handleEvent(event):
					pygame.event.clear()
					file_list = glob.glob(TEMP_LIST)
					if FILE_PRINTER in file_list:
						pygame.draw.rect(screen, BLACK, (0,(HEIGHT_DISPLAY-200),WIDTH_DISPLAY,(HEIGHT_DISPLAY-(HEIGHT_DISPLAY-200))),0) 				#WHITE rectangle for brightness value
						screen.blit(pygame.font.SysFont("freeserif",40,bold=1).render("Voulez-vous valider vos reglages ?", 1, WHITE),(0,HEIGHT_DISPLAY-190))
						yes_button.draw(screen)
						no_button.draw(screen)
					elif FILE_SETUP in file_list:
						DrawMessage("Veuillez imprimer la photo",400,70,100,100,20,BLACK)
					else:
						DrawMessage("Veuillez prendre une photo",400,70,100,100,20,BLACK)
				
				if 'click' in yes_button.handleEvent(event):
					DrawMessage("WAIT...",400,70,100,100,40,BLACK)
					loop_printerSetUp = False
					loop_gallery = True	
				
				if 'click' in no_button.handleEvent(event):
					LoadImageObjectToScreen(object_list[0])	#load init image
					print_button.draw(screen)
					contrast_more_button.draw(screen)
					contrast_less_button.draw(screen)
					brightness_more_button.draw(screen)
					brightness_less_button.draw(screen)
					take_pic_button.draw(screen)
					skip_button.draw(screen)
					quit_button.draw(screen)
					validate_button.draw(screen)
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-500),240,60),0) 				#WHITE rectangle for contrast title
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-350),240,60),0) 				#WHITE rectangle for brightness title
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-440),80,60),0) 				#WHITE rectangle for contrast value
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-290),80,60),0) 				#WHITE rectangle for brightness value
					screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("CONTRASTE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-500))
					screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("LUMINOSITE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-350))
					screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(contrast_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-440))
					screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(brightness_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-290))
					DrawMessage("Prenez une photo et reglez la luminosite et le contraste.",WIDTH_DISPLAY,(HEIGHT_DISPLAY-(HEIGHT_DISPLAY-100)),0,(HEIGHT_DISPLAY-100),25,BLACK)#(message,WIDTH_DISPLAY,HEIGHT_DISPLAY,x,y,size)
					file_list = glob.glob(TEMP_LIST)
					if FILE_SETUP_TEMP in file_list:
						ConvertPictureForDisplay(screen, FILE_SETUP_TEMP)
					elif FILE_SETUP in file_list:
						ConvertPictureForDisplay(screen, FILE_SETUP)
				
				if 'click' in take_pic_button.handleEvent(event) and waiting_on_download == False:
					SmileTimer()
					TakePicture(app_name, TEMP_PATH)
					RenderOverlay(app_name)
					contrast_value = 1.0
					brightness_value = 1.0
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-500),240,60),0) 				#WHITE rectangle for contrast title
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-380),(HEIGHT_DISPLAY-350),240,60),0) 				#WHITE rectangle for brightness title
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-440),80,60),0) 				#WHITE rectangle for contrast value
					pygame.draw.rect(screen, WHITE, ((WIDTH_DISPLAY-300),(HEIGHT_DISPLAY-290),80,60),0) 				#WHITE rectangle for brightness value
					screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("CONTRASTE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-500))
					screen.blit(pygame.font.SysFont("freeserif",35,bold=1).render("LUMINOSITE", 1, BLACK),(WIDTH_DISPLAY-380,HEIGHT_DISPLAY-350))
					screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(contrast_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-440))
					screen.blit(pygame.font.SysFont("freeserif",45,bold=1).render(str(brightness_value), 1, BLACK),(WIDTH_DISPLAY-300,HEIGHT_DISPLAY-290))
					DrawMessage("Prenez une photo et reglez la luminosite et le contraste.",WIDTH_DISPLAY,(HEIGHT_DISPLAY-(HEIGHT_DISPLAY-100)),0,(HEIGHT_DISPLAY-100),25,BLACK)#(message,WIDTH_DISPLAY,HEIGHT_DISPLAY,x,y,size)

				if 'click' in print_button.handleEvent(event):
					file_list = glob.glob(TEMP_LIST)
					if FILE_SETUP_TEMP in file_list:
						resize_img = pygame.transform.scale(pygame.image.load(FILE_SETUP_TEMP), (WIDTH_PRINTER,HEIGHT_PRINTER))
						pygame.image.save(resize_img,FILE_PRINTER)
						try:
							print_command = "lp -d Brother_QL-800 " + FILE_PRINTER
							p = sub.Popen(print_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
							DrawMessage("impression en cours",200,20,0,0,10,BLACK)
						except:
							print("issue in printing")	
	#ADD PRINTER THREAD				
					elif FILE_SETUP in file_list:
						resize_img = pygame.transform.scale(pygame.image.load(FILE_SETUP), (WIDTH_PRINTER,HEIGHT_PRINTER))
						pygame.image.save(resize_img,FILE_PRINTER)
						try:
							print_command = "lp -d Brother_QL-800 " + FILE_PRINTER
							p = sub.Popen(print_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
							DrawMessage("impression en cours",200,20,0,0,10,BLACK)
						except:
							print("issue in printing")
					else:
						DrawMessage("Veuillez prendre une photo",400,70,100,100,20,BLACK)

				if 'click' in contrast_more_button.handleEvent(event):
					file_list = glob.glob(TEMP_LIST)
					if FILE_SETUP in file_list:
						contrast_value = contrast_value + 0.25
						DrawMessage("WAIT...",400,70,100,100,40,BLACK)
						GreyPictureSetUp(FILE_SETUP, FILE_SETUP_TEMP)
						ConvertPictureForDisplay(screen, FILE_SETUP_TEMP)
					else:
						DrawMessage("Veuillez prendre une photo",400,70,100,100,20,BLACK)
				
				if 'click' in contrast_less_button.handleEvent(event) and contrast_value > 0.0:
					file_list = glob.glob(TEMP_LIST)
					if FILE_SETUP in file_list:
						contrast_value = contrast_value - 0.25
						DrawMessage("WAIT...",400,70,100,100,40,BLACK)
						GreyPictureSetUp(FILE_SETUP, FILE_SETUP_TEMP)	
						ConvertPictureForDisplay(screen, FILE_SETUP_TEMP)				
					else:
						DrawMessage("Veuillez prendre une photo",400,70,100,100,20,BLACK)

				if 'click' in brightness_more_button.handleEvent(event):
					file_list = glob.glob(TEMP_LIST)
					if FILE_SETUP in file_list:
						brightness_value = brightness_value + 0.25
						DrawMessage("WAIT...",400,70,100,100,40,BLACK)
						GreyPictureSetUp(FILE_SETUP, FILE_SETUP_TEMP)	
						ConvertPictureForDisplay(screen, FILE_SETUP_TEMP)				
					else:
						DrawMessage("Veuillez prendre une photo",400,70,100,100,20,BLACK)
				
				if 'click' in brightness_less_button.handleEvent(event) and brightness_value > 0.0:
					file_list = glob.glob(TEMP_LIST)
					if FILE_SETUP in file_list:
						brightness_value = brightness_value - 0.25
						DrawMessage("WAIT...",400,70,100,100,40,BLACK)
						GreyPictureSetUp(FILE_SETUP, FILE_SETUP_TEMP)
						ConvertPictureForDisplay(screen, FILE_SETUP_TEMP)						
					else:
						DrawMessage("Veuillez prendre une photo",400,70,100,100,20,BLACK)
				pygame.display.update()
				pygame.event.clear()			#remove all other clic in the queue.

		files = glob.glob(TEMP_PATH + "/*")
		for f in files:		#remove */temp/ files
			os.remove(f)
#LOOP GALLERY------------------------------------------------------------------------------------------------------------------------------------------------
	if loop_gallery:
		app_name = "Fiebooth V2_GALLERY"
		OpenBasicWindow(app_name)
		pygame.display.update()

		try:
			while(loop_gallery):
				if GPIO.input(BP_PIN) == 0:
					sleep(0.05)						#debounce time (in seconds)
					if GPIO.input(BP_PIN) == 0:
						SmileTimer()
						TakePicture(app_name, PICTURES_PATH)

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						loop_gallery = False
						app_status = False

					if 'click' in take_pic_button.handleEvent(event):
						SmileTimer()
						TakePicture(app_name, PICTURES_PATH)
						
					if 'click' in quit_button.handleEvent(event):
						loop_gallery = False
						app_status = False

					#¤v3 L+ sans L-
					if 'click' in brightness_more_button_small.handleEvent(event):
						brightness_value = brightness_value+0.25
						logging.info("augmentation Luminosité")
                        addPreviewOverlay(20,200,35,"lumi +"+str(brightness_value))
                        time.sleep(1)

					#¤v3 L- sans L+
					if 'click' in brightness_less_button_small.handleEvent(event):
						brightness_value = brightness_value-0.25
						if brighten<0:
							brightness_value=0
						logging.info("diminution Luminosité")
                        addPreviewOverlay(20,200,35,"lumi -"+str(brightness_value))
                        time.sleep(1)

					#¤v3 Quitter si L+ et L- ????
					if 'click' in brightness_more_button_small.handleEvent(event) and 'click' in brightness_less_button_small.handleEvent(event):
						loop_gallery = False
						app_status = False

				if waiting_on_download and os.path.isfile(last_image_taken):
					change_ticks = pygame.time.get_ticks() + SHOW_PICTURE_TIME #sets a XX second timeout before the slideshow continues
					LoadNewImage()
				
				if waiting_on_print :
					PrintPicture()
					# if PrintPicture() == True:
					# 	thread_1 = PrinterThread()
					# 	thread_1.start()
					# 	thread_1.join()

				if change_ticks  < pygame.time.get_ticks():
					# if len(os.listdir("/home/pi/Downloads/FieboothV2/images")) > 0:
					# 	if current_image%3 > 0:
					# 		LoadImageObjectToScreen(object_list[0])
					# 	else:
					# 		NextPicture()
					# 		LoadImageObjectToScreen(object_list[current_image])
					# 		RenderOverlay()
					NextPicture()
					LoadImageObjectToScreen(object_list[current_image])
					RenderOverlay(app_name)
					
					change_ticks = pygame.time.get_ticks() + SHOW_GALLERY_TIME		# XX seconds and then flip to the next image
			pygame.display.update()	
		except:
			print ("EXCEPTION in main")
			app_status = False
			loop_gallery = False
#DEBUG#print ("process complete")
print_command = "cancel -a"  											#Cancel all printer jobs
p = sub.Popen(print_command,stdout=sub.PIPE,stderr=sub.PIPE,shell=True) #COMMAND LINE cancel all printer jobs
pygame.quit()