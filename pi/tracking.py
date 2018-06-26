import cv2 as cv
import numpy as np

# Real width of your object
REAL_WIDTH = 5

# Focal length of your camera
# Focal length = (Width in pixels *  Distance to object) / Width of an object
FOCAL_LENGTH = 832

# Distance to object = Focal length * Width of an object / Width in pixels
def distance(pixel_width, real_width, focal_length):
	return round(focal_length * real_width / pixel_width)	
	
def steering_decision(frame, lower, upper, tolerance, height, width):
	frame = cv.GaussianBlur(frame, (5, 5), 0)
	#  Convert frame from BGR to HSV color space
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	# Apply our filter
	mask = cv.inRange(hsv, lower, upper)

	# Find all contours
	contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	# If at least one contour exist
	if len(contours) != 0:
		# Find contour with max area
		cnt = max(contours, key = cv.contourArea)

		# Filter noize contours
		if cv.contourArea(cnt) > 500:
			# Find and draw a bounding rectangle
			x,y,w,h = cv.boundingRect(cnt)
			# Find center of a bounding rectangle
			center = (int(x+w/2), int(y+h/2))
			# Where to move decision
			if abs(center[0] - width / 2) > tolerance:
				if center[0] - width / 2 > 0:
					return "right" , w
				else:
					return "left", w
			else:
				return "stay", w
	return "no_object", 0,  	