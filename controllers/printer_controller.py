

import time
from config import config
from utils.file_utils import FileUtils
import cups
import subprocess
import pygame
import os
import time
import logging

class PrinterController():
	
	def __init__(self):
		self.logger = logging.getLogger("fiebooth")
		pass
	
	def print(self, image_path):
		#create temp directory
		
		tmp_dir = FileUtils.get_temp_dir()
		self.logger.info(f"folder name {tmp_dir}")
		tmp_img = os.path.join(tmp_dir, f"fb_{int(time.time())}.png")
		resize_img = pygame.transform.scale(pygame.image.load(image_path),(config.WIDTH_PRINTER, config.HEIGHT_PRINTER))
		pygame.image.save(resize_img, tmp_img)
		self.logger.info(f"temp file {tmp_img} saved before printing")
		# send print to printer
		print_command = f"lp -d Brother_QL-800 {tmp_img}"
		p = subprocess.Popen(print_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
	
	def status(self):
		init_time = time.clock()
		current_time = init_time
		#print("Initial time : ", init_time)
		printer_status = "IDLE"
		
		#file1 = open("printerLogs.txt","a")
		while current_time < (init_time + float(config.TIMEOUT)) and printer_status != "PRINTING COMPLET":
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