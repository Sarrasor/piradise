import cv2 as cv
import numpy as np
import time
import RPi.GPIO as GPIO
import sys
import select

import tracking
import drive

# Frame size
HEIGHT = 240
WIDTH = 320

#Filter
LOWER = np.array([68, 65, 31])
UPPER = np.array([100, 229, 167])

# Start capture
cap = cv.VideoCapture(0)
cap.set(3, WIDTH)  # 3 CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
cap.set(4, HEIGHT) # 4 CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream. 

# Real width of your object
REAL_WIDTH = 5

# Focal length of your camera
# Focal length = (Width of an object in pixels *  Distance to object) / Real width of an object
FOCAL_LENGTH = 416

# Desired distance
DESIRED_DISTANCE = 10
# Desired distance's tolerance
DESIRED_DISTANCE_TOLERANCE = 0

# How tolerant our tracker is
STEERING_TOLERANCE = 30

# Prepare motors
drive.motor_setup()

while True:
	ret, frame = cap.read()

	decision, pixel_width = tracking.steering_decision(frame, LOWER, UPPER, STEERING_TOLERANCE, HEIGHT, WIDTH)

	if pixel_width != 0:
		distance_prediction = tracking.distance(pixel_width, REAL_WIDTH, FOCAL_LENGTH)
	else:
		distance_prediction = "No object"	

	print(decision, distance_prediction)

	# Actions, based on previous decision
	if decision == "stay":
		drive.stop()
	elif decision == "left":
		drive.turn_left(0.01)
	elif decision == "right":
		drive.turn_right(0.01)
	else:
		drive.stop()	

	if distance_prediction != "No object":	
		if abs(distance_prediction - DESIRED_DISTANCE) > DESIRED_DISTANCE_TOLERANCE:
			if distance_prediction - DESIRED_DISTANCE < 0:
				drive.backward(0.015)
			else:
				drive.forward(0.015)
		else:
			drive.stop()			

	# Break on key pressed 
	if select.select([sys.stdin,],[],[],0.0)[0]:
		break	

# Release camera
time.sleep(0.5)
cap.release()
GPIO.cleanup()
time.sleep(1)




