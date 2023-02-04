import time
import digitalio
import board
import adafruit_matrixkeypad

rows = [digitalio.DigitalInOut(x) for x in (board.D25, board.D8, board.D7, board.D1)]
cols = [digitalio.DigitalInOut(x) for x in (board.D12, board.D16, board.D20, board.D21)]
keys = (("1", "2", "3", "A"),
        ("4", "5", "6", "B"),
        ("7", "8", "9", "C"),
        ('*', "0", '#', "D"))

keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

def hearing():
	keys = keypad.pressed_keys
	# print("hearing in ada called")
	if keys :
		# print("entered if from keys")
		for char in keys :
			# print("entered for = ",char, "\t", keys)
			if (char in keys) :
				# print("char in keys")
				time.sleep(0.15)
				# print("return from ada =",char[0])
				return char[0]
				break
	else:
		time.sleep(0.1)
		return None	 

	


		

# while True:
#     # print(hearing())
# 	getpin()


# while True:
# 	b= hearing()
# 	if (b!= None):
# 		print (b)
# 		# break