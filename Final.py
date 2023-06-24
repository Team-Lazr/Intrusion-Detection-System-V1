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


###############_INTERUPT_###############

def interupt_create():
	global intcreated
	if(intcreated==False):
		print("interupt_create called")
		GPIO.add_event_detect(limitsw_pin, GPIO.FALLING, callback=intrusion, bouncetime=150) #Create Interrupt to execute the function when a falling edge is detected
		intcreated = True
	

def interupt_destroy():
	global intcreated
	GPIO.remove_event_detect(limitsw_pin) #Remove Interrupt
	print("interupt_destroy called")
	intcreated = False

###############_INTERUPT_###############





def intrusion(aaaa): #Function to sound Alarm if Intruder is Detected
	global intruder
	intruder = True

	elapsed_time = 0
	start_time = 0
	start_time = time.time()
	print(start_time)	


	interupt_destroy() #Disable interrupt to avoid calling of function multiple times
	print("Intruder Detected")
	lcd.clear()
	lcd.message("Intruder \nPress A - PIN") #Update Display

	while intruder:
		b = time.time()
		elapsed_time = (b - start_time)
		a = int(elapsed_time)
		print(a,type(a))
		if(a>10): #If no Pin is entered till 10 seconds, activate the buzzer
			GPIO.output(alarm_pin, 1)
			time.sleep(0.1)
			GPIO.output(alarm_pin, 0)
			time.sleep(0.1)
		if(keypad.hearing()=="A"): #Check if "A" was pressed
			print("getpin() Called")
			pin = getpin() #Fetch the pin entered
			if (pin in master_pin): #Check if pin is correct
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
					upload.sheetsupdate("Buzzout","PIN","Access Granted") #Update Google Sheet
					print("Access Granted")
				else :
					upload.sheetsupdate("Intruder Detected","PIN","Access Granted") #Update Google Sheet
					print("Intruder Access Granted")
				time.sleep(2)
				lcd.clear()
				lcd.message("A - PIN \nB - Fingerprint") #Wait for User Interaction

				intruder = False
				
				break
			else:
				lcd.clear()
				lcd.message("Intruder Alert\nWrong Pin") #If pin is wrong
				upload.sheetsupdate("Intruder Detected","PIN","Access Denied") #Update Google Sheet





def getpin(): #Function to Fetch Pin from user
	lcd.clear()
	lcd.message("Enter Pin: ") #Update Screen
	pin = ""
	while True:
		data = ""
		data = keypad.hearing()
		if(data == "C"): #Clear Screen if user presses "C" | incase wrong pin is entered
			print("Clear screen")
			lcd.clear()
			lcd.message("Cleared")
			time.sleep(0.5)
			lcd.clear()
			lcd.message("Enter Pin: ")
			pin = ""
			data = None
		elif(data == "D"): # Go to home if user pressed "D" | Cancel Operation
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
			pin = pin + data #Append Data
			lcd.message("*") #Update LCD

			if (len(pin) == 4): #If 4 Digit received
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

while True: #Main While Loop
	if(intruder == False):
		interupt_create() #Initialize Interrupt
		heard = keypad.hearing() #Check for Keypress
		if(heard=="A"): #If "A" is pressed | Pin Option
			print("heard A")
			lcd.clear()
			lcd.message("Enter Pin: ")
			while True :
				if(attempt_counter < 3) : #Check if Attemp Counter is less than 3
					lcd.clear()
					lcd.message("Enter Pin: ")
					pin = getpin() #Fetch Pin
					print("Pin = ", pin)
					if (pin in master_pin) :
						lcd.clear()
						lcd.message("Access Granted")
						attempt_counter = 0
						
						interupt_destroy() # Disable interrupt to allow the user to pass through

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						upload.sheetsupdate("IN","PIN","Access Granted") #Update google sheets
						time.sleep(5)

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						interupt_create() # Enable interrupt

						lcd.clear()
						lcd.message("A - PIN \nB - Fingerprint")
						break
					elif(pin=='d'): # User cancelled operation
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
						lcd.message("A - PIN \nB - Fingerprint") #Back to home Screen
						break
					else:
						attempt_counter += 1 #If Wrong pin is entered
						lcd.clear()
						lcd.message("Wrong Pin!!\nAttempts Left:{}".format(3-attempt_counter)) # Print No. of Attempts Left
						time.sleep(1)
						for i in range(5) :
							GPIO.output(alarm_pin, 1)
							time.sleep(0.25)
							GPIO.output(alarm_pin, 0)
							time.sleep(0.25)
						upload.sheetsupdate("IN","PIN","Access Denied, Attempt No: {}".format(attempt_counter)) #Update google sheets
				else : #If more than 3 failed attempts are made
					upload.sheetsupdate("IN","PIN","System Locked for 10 Seconds") #Update google sheets
					attempt_counter = 0 #Reset Counter
					lcd.clear()
					for i in range(10):
						time.sleep(1)
						lcd.clear()
						lcd.message("Locked \nTime Left = {}  ".format(10-i)) #Lock System for 10 Seconds
					lcd.clear()
					lcd.message("A - PIN \nB - Fingerprint")
					break
						

		elif(heard=="B"): # If "B" is Pressed | Fingerprint Option
			
			while True :
				if(attempt_counter < 3) :# Check No. of Attempts
					lcd.clear()
					lcd.message("Scan your \n Fingerprint:")
					scan_fing=fp.get_fingerprint() #Check if Fingerprint is Registered
					if (scan_fing) :
						lcd.clear()
						lcd.message("Match! \nAccess Granted")
						attempt_counter = 0

						interupt_destroy() #Disable interupt to let the user pass through

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						upload.sheetsupdate("IN","Fingerprint","Access Granted") # Update google sheets
						time.sleep(5)

						GPIO.output(alarm_pin, 1)
						time.sleep(1)
						GPIO.output(alarm_pin, 0)

						interupt_create() # Enable Interrupt

						lcd.clear()
						lcd.message("A - PIN \nB - Fingerprint") #Back to home Screen
						break
					else:#If Wrong pin is entered
						attempt_counter += 1
						upload.sheetsupdate("IN","Fingerprint","Access Denied, Attempt No: {}".format(attempt_counter))#Update google sheets
						lcd.clear()
						lcd.message("No Match!\nAttempts Left:{}".format(3-attempt_counter))# Print No. of Attempts Left
						for i in range(5) :
							GPIO.output(alarm_pin, 1)
							time.sleep(0.25)
							GPIO.output(alarm_pin, 0)
							time.sleep(0.25)
						time.sleep(1)
						
							
				else :#If more than 3 failed attempts are made
					upload.sheetsupdate("IN","Fingerprint","System Locked for 10 Seconds")#Update google sheets
					lcd.clear()
					for i in range(10):
						lcd.clear()
						lcd.message("Locked \nTime Left = {}  ".format(10-i))#Lock System for 10 Seconds
						time.sleep(1)
						attempt_counter = 0
					lcd.clear()
					lcd.message("A - PIN \nB - Fingerprint")
					break

##################_END_OF_MAIN_##################