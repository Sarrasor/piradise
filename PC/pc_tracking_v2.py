import cv2 as cv
import numpy as np

# Frame size
# Less the size, simpler to process
# Crucial on Raspberry Pi
HEIGHT = 480
WIDTH = 640

# Display functions:
# Press W - to turn steering decision on/off
# Press E - to turn stay boundaries on/off
# Press R - to show result values
# Press T - to turn precise contour on/off
# Press Y - to turn center of a contour on/off
# Press I - to show info message
# Press U - to turn bounding rectangle on/off


# Show steering decision on original frame
SHOW_DECISION = True
# Show "Stay" boundaries 
SHOW_STAY_BOUNDARIES = True
# Show bounding rectangle
SHOW_RECTANGLE = True
# Show precise contour
SHOW_PRECISE = True
# Show center of a contour
SHOW_CENTER = True
# Show info message
SHOW_INFO = True
# Show result values
SHOW_RESULT = False

# HSV Filter 
LOWER = np.array([33, 60, 82])
UPPER = np.array([98, 255, 255])

# How tolerant our tracker is
# In other words, this value defines "Stay" position boundaries
TOLERANCE = 25

# Font. Not all fonts are supported
# Check OpenCV documentation
FONT = cv.FONT_HERSHEY_SIMPLEX

# Filter contours with small area
NOIZE_AREA = 500


# Connect to camera
# If you have more than one camera connected
# Change 0 to 1 to choose second camera on so on
cap = cv.VideoCapture(0)
# Resize capture
cap.set(3, WIDTH)  # 3 =  CV_CAP_PROP_FRAME_WIDTH (Width of the frames in the video stream)
cap.set(4, HEIGHT) # 4 =  CV_CAP_PROP_FRAME_HEIGHT (Height of the frames in the video stream) 

# Create a window for sliders and frames
cv.namedWindow("Tracking", cv.WINDOW_FULLSCREEN)

# Event function for trackbars
def nothing(x):
    pass

# Create trackbars for color change
cv.createTrackbar("Lower hue", "Tracking", LOWER[0], 255, nothing)
cv.createTrackbar("Upper hue", "Tracking", UPPER[0], 255, nothing)
cv.createTrackbar("Lower saturation", "Tracking", LOWER[1], 255, nothing)
cv.createTrackbar("Upper saturation", "Tracking", UPPER[1], 255, nothing)
cv.createTrackbar("Lower value", "Tracking", LOWER[2], 255, nothing)
cv.createTrackbar("Upper value", "Tracking", UPPER[2], 255, nothing)
# Trackbar for tolerance
cv.createTrackbar("Tolerance", "Tracking", TOLERANCE, int(WIDTH/2), nothing)
# Trackbar for noize area
cv.createTrackbar("Noize area", "Tracking", NOIZE_AREA, int(HEIGHT*WIDTH/5), nothing)

# Info message 
info1 = 'Press Q to exit, W - steering decision, E - "Stay" boundaries'
info2 = "U - bounding rectangle, T - precise contour, Y - center of a contour"
info3 = "I - this message, R - result. WERTYUI keys work as on/off button"

# Result message
result1 = "Filter:  Lower is " + str(LOWER) + " Upper is " + str(UPPER)
result2 = "Tolerance: " + str(TOLERANCE)
result3 = "Noize area: " + str(NOIZE_AREA)

while True:
	# Read camera frame
	ret, frame = cap.read()
	# Save original frame
	original = frame

	# Blur a frame a litttle bit to remove noize
	frame = cv.GaussianBlur(frame, (5, 5), 0)
	#  Convert frame from BGR to HSV color space
	hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
	# Apply our filter
	mask = cv.inRange(hsv, LOWER, UPPER)

	# Find all contours
	img, contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	# If at least one contour exist
	if len(contours) != 0:
		# Find contour with max area
		cnt = max(contours, key = cv.contourArea)

		# Filter noize contours
		if cv.contourArea(cnt) > NOIZE_AREA:
			# Find and draw a bounding rectangle
			x,y,w,h = cv.boundingRect(cnt)
			# print(x, y, w, h)
			if SHOW_RECTANGLE:
				cv.rectangle(original, (x,y), (x+w,y+h), (0,255,0), 1)
			# Find center of a bounding rectangle
			center = (int(x+w/2), int(y+h/2))
			# Draw a center circle
			if SHOW_CENTER:
				cv.circle(original, (center[0], center[1]), 3, (0,0,255), -1)
			# Calculate the x-center of a frame
			xc = int(original.shape[1] / 2)

			# Draw "Stay" boundaries
			if SHOW_STAY_BOUNDARIES:
				cv.line(original, (xc+TOLERANCE, 0), (xc+TOLERANCE, original.shape[0]), (0, 255, 255), 1)
				cv.line(original, (xc-TOLERANCE, 0), (xc-TOLERANCE, original.shape[0]), (0, 255, 255), 1)

			if SHOW_DECISION: 
				# Where to move decision
				original[:45, :100].fill(0)

				if abs(center[0] - xc) > TOLERANCE:
					if center[0] - xc > 0:
						cv.putText(original,"Right", (10,30), FONT, 1, (255,255,255), 2)
					else:
						cv.putText(original,"Left", (10,30), FONT, 1, (255,255,255), 2)
				else:
					cv.putText(original,"Stay", (10,30), FONT, 1, (255,255,255), 2)	


			if SHOW_PRECISE:		
				# Find and draw precise contour
				rect = cv.minAreaRect(cnt)
				box = cv.boxPoints(rect)
				box = np.int0(box)
				cv.drawContours(original, [box], 0, (255,0,0), 1)

	# Show info message
	if SHOW_INFO:
		original[HEIGHT-80:, :].fill(0)

		cv.putText(original, info1, (5, HEIGHT - 60), FONT, 0.55, (255,255,255), 0)
		cv.putText(original, info2, (5, HEIGHT - 40), FONT, 0.55, (255,255,255), 0)
		cv.putText(original, info3, (5, HEIGHT - 20), FONT, 0.55, (255,255,255), 0)

	# Show result
	if SHOW_RESULT:
		original[HEIGHT-150:HEIGHT-80, :].fill(0)

		result1 = "Filter:  Lower is " + str(LOWER) + " Upper is " + str(UPPER)
		result2 = "Tolerance: " + str(TOLERANCE)
		result3 = "Noize area: " + str(NOIZE_AREA)

		cv.putText(original, result1, (5, HEIGHT - 130), FONT, 0.55, (255,255,255), 0)
		cv.putText(original, result2, (5, HEIGHT - 110), FONT, 0.55, (255,255,255), 0)
		cv.putText(original, result3, (5, HEIGHT - 90), FONT, 0.55, (255,255,255), 0)

 	# Convert mask from GRAY to BGR in order to concatenate it with original frame
	mask = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
	# Concatenate mask and original frame to show it in one window
	numpy_horizontal = np.hstack((mask, original)) 
	cv.imshow("Tracking", numpy_horizontal)

	# Wait for a key
	key = cv.waitKey(1)

	# Key logic
	if key == 113:
		break
	elif key == 119:	
		SHOW_DECISION = not SHOW_DECISION
	elif key == 101:
		SHOW_STAY_BOUNDARIES = not SHOW_STAY_BOUNDARIES
	elif key == 114:
		SHOW_RESULT = not SHOW_RESULT
	elif key == 116:
		SHOW_PRECISE = not SHOW_PRECISE
	elif key == 121:
		SHOW_CENTER = not SHOW_CENTER	
	elif key == 105:
		SHOW_INFO = not SHOW_INFO	
	elif key == 117:
		SHOW_RECTANGLE = not SHOW_RECTANGLE	

	# get current positions of trackbars
	lh = cv.getTrackbarPos("Lower hue", "Tracking")
	ls = cv.getTrackbarPos("Lower saturation", "Tracking")
	lv = cv.getTrackbarPos("Lower value", "Tracking")
	uh = cv.getTrackbarPos("Upper hue", "Tracking")
	us = cv.getTrackbarPos("Upper saturation", "Tracking")
	uv = cv.getTrackbarPos("Upper value", "Tracking")
	# Apply new filter values
	LOWER = np.array([lh, ls, lv])
	UPPER = np.array([uh, us, uv])
	
	# Apply new Tolerance value
	TOLERANCE = cv.getTrackbarPos("Tolerance", "Tracking") 

	# Apply new Noize area
	NOIZE_AREA = cv.getTrackbarPos("Noize area", "Tracking") 

# Release camera and close windows
cap.release()
cv.destroyAllWindows()		