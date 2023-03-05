"""

INTRUSION DETECTION SYSTEM

This Code is Written by Students of Group 2

Harsh Buddhadev(D003)
Abhishek Garg(D007)
Krish Gosaliya(D009)
Akshit Gupta(D010)

"""


import RPi.GPIO as GPIO
import time
import upload
import check_fingerprint as fp
import ada_keypad as keypad
from Adafruit_CharLCD import Adafruit_CharLCD


GPIO.cleanup()

GPIO.setmode(GPIO.BCM)
lcd = Adafruit_CharLCD(rs=26, en=19,d4=13, d5=6, d6=5, d7=0,cols=16, lines=2)
limitsw_pin = 9
alarm_pin = 11


global intcreated
intcreated = False
global intruder
intruder = False

intialized = False

######_PIN_#####
master_pin = ["5555", "1234", "4321"]
######_PIN_#####

GPIO.setup(alarm_pin, GPIO.OUT)
GPIO.setup(limitsw_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


###############_INTERUPT_CREATE_DESTROY_###############

def interupt_create():
	global intcreated
	if(intcreated==False):
		print("interupt_create called")
		GPIO.add_event_detect(limitsw_pin, GPIO.FALLING, callback=intrusion, bouncetime=150)
		intcreated = True
	

def interupt_destroy():
	global intcreated
	GPIO.remove_event_detect(limitsw_pin)
	print("interupt_destroy called")
	intcreated = False

###############_INTERUPT_CREATE_DESTROY_###############





def intrusion(aaaa):
	global intruder
	intruder = True

	elapsed_time = 0
	start_time = 0
	start_time = time.time()
	print(start_time)	


	interupt_destroy()
	print("Intruder Detected")
	lcd.clear()
	lcd.message("Intruder \nPress A - PIN")

	while intruder:
		b = time.time()
		elapsed_time = (b - start_time)
		a = int(elapsed_time)
		print(a,type(a))
		if(a>10):
			GPIO.output(alarm_pin, 1)
			time.sleep(0.1)
			GPIO.output(alarm_pin, 0)
			time.sleep(0.1)
		if(keypad.hearing()=="A"):
			print("getpin() Called")
			pin = getpin()
			if (pin in master_pin):
				print("Alarm Disarmed")

				GPIO.output(alarm_pin, 1)
				time.sleep(0.1)
				GPIO.output(alarm_pin, 0)
				time.sleep(0.1)
				GPIO.output(alarm_pin, 1)
				time.sleep(0.1)
				GPIO.output(alarm_pin, 0)
				time.sleep(0.1)
				if(a<10):
					upload.sheetsupdate("Buzzout","PIN","Access Granted")
					print("Access Granted")
				else :
					upload.sheetsupdate("Intruder Detected","PIN","Access Granted")
					print("Intruder Access Granted")
				time.sleep(2)
				lcd.clear()
				lcd.message("A - PIN \nB - Fingerprint")

				intruder = False
				
				break
			else:
				lcd.clear()
				lcd.message("Intruder Alert\nWrong Pin")
				upload.sheetsupdate("Intruder Detected","PIN","Access Denied")





def getpin():
	lcd.clear()
	lcd.message("Enter Pin: ")
	pin = ""
	while True:
		data = ""
		data = keypad.hearing()
		if(data == "C"):
			print("Clear screen")
			lcd.clear()
			lcd.message("Cleared")
			time.sleep(0.5)
			lcd.clear()
			lcd.message("Enter Pin: ")
			pin = ""
			data = None
		elif(data == "D"):
			if(intruder==True):
				continue
			else:
				data = None
				pin = ""
				print("Home")
				lcd.clear()
				lcd.message("Home")
				time.sleep(1)
				lcd.clear()
				return "d"
				break

		elif(data == "A" or data == "B"):
			data = None
       

		if(data != None):
			pin = pin + data
			lcd.message("*")

			if (len(pin) == 4):
				print("len=4")
				print("Pin:",pin)
				return pin
				break




##################_START_OF_MAIN_##################

if(intialized == False):
	lcd.clear()
	lcd.message("A - PIN\nB - Fingerprint")
	interupt_create()
	attempt_counter = 0
	intialized = True

while True:
	if(intruder == False):
		interupt_create()
		heard = keypad.hearing()
		if(heard=="A"):
			print("heard A")
			lcd.clear()
			lcd.message("Enter Pin: ")
			while True :
				if(attempt_counter < 3) :
					lcd.clear()
					lcd.message("Enter Pin: ")
					pin = getpin()
					print("Pin = ", pin)
					if (pin in master_pin) :
						lcd.clear()
						lcd.message("Access Granted")
						attempt_counter = 0
						
						interupt_destroy()

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						upload.sheetsupdate("IN","PIN","Access Granted")
						time.sleep(5)

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						interupt_create()

						lcd.clear()
						lcd.message("A - PIN \nB - Fingerprint")
						break
					elif(pin=='d'):
						print("HOME")
						GPIO.output(alarm_pin, 1)
						time.sleep(0.1)
						GPIO.output(alarm_pin, 0)
						time.sleep(0.1)
						GPIO.output(alarm_pin, 1)
						time.sleep(0.1)
						GPIO.output(alarm_pin, 0)
						time.sleep(0.1)
						lcd.clear()
						lcd.message("A - PIN \nB - Fingerprint")
						break
					else:
						attempt_counter += 1
						lcd.clear()
						lcd.message("Wrong Pin!!\nAttempts Left:{}".format(3-attempt_counter))
						time.sleep(1)
						for i in range(5) :
							GPIO.output(alarm_pin, 1)
							time.sleep(0.25)
							GPIO.output(alarm_pin, 0)
							time.sleep(0.25)
						upload.sheetsupdate("IN","PIN","Access Denied, Attempt No: {}".format(attempt_counter))			
				else :
					upload.sheetsupdate("IN","PIN","System Locked for 10 Seconds")
					attempt_counter = 0
					lcd.clear()
					for i in range(10):
						time.sleep(1)
						lcd.clear()
						lcd.message("Locked \nTime Left = {}  ".format(10-i))
					lcd.clear()
					lcd.message("A - PIN \nB - Fingerprint")
					break
						

		elif(heard=="B"):
			
			while True :
				if(attempt_counter < 3) :
					lcd.clear()
					lcd.message("Scan your \n Fingerprint:")
					scan_fing=fp.get_fingerprint()
					if (scan_fing) :
						lcd.clear()
						lcd.message("Match! \nAccess Granted")
						attempt_counter = 0

						interupt_destroy()

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						upload.sheetsupdate("IN","Fingerprint","Access Granted")
						time.sleep(5)

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						interupt_create()

						lcd.clear()
						lcd.message("A - PIN \nB - Fingerprint")
						break
					else:
						attempt_counter += 1
						upload.sheetsupdate("IN","Fingerprint","Access Denied, Attempt No: {}".format(attempt_counter))
						lcd.clear()
						lcd.message("No Match!\nAttempts Left:{}".format(3-attempt_counter))
						for i in range(5) :
							GPIO.output(alarm_pin, 1)
							time.sleep(0.25)
							GPIO.output(alarm_pin, 0)
							time.sleep(0.25)
						time.sleep(1)
						
							
				else :
					upload.sheetsupdate("IN","Fingerprint","System Locked for 10 Seconds")
					lcd.clear()
					for i in range(10):
						lcd.clear()
						lcd.message("Locked \nTime Left = {}  ".format(10-i))
						time.sleep(1)
						attempt_counter = 0
					lcd.clear()
					lcd.message("A - PIN \nB - Fingerprint")
					break

##################_END_OF_MAIN_##################

