import time
import board
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import serial

port="/dev/serial0"
uart = serial.Serial(port, baudrate=57600, timeout=1) #Init Serial Port
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():
	if finger.read_templates() != adafruit_fingerprint.OK:
		raise RuntimeError("Failed to read templates")
	while finger.get_image() != adafruit_fingerprint.OK:
		pass
	if finger.image_2_tz(1) != adafruit_fingerprint.OK:
		return False
	if finger.finger_search() != adafruit_fingerprint.OK:
		return False
	return True
 
if __name__ == "__main__":
	while True:
		if get_fingerprint():
			print("Detected fingerprint")
		else:
			print("Finger not found")