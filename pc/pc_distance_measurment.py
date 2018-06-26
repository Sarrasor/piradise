import cv2 as cv
import numpy as np

# Frame size
# Less the size, simpler to process
# Crucial on Raspberry Pi
HEIGHT = 480
WIDTH = 640

# HSV Filter 
LOWER = np.array([68, 65, 31])
UPPER = np.array([100, 229, 167])

# How tolerant our tracker is
# In other words, this value defines "Stay" position boundaries
TOLERANCE = 25

# Filter contours with small area
NOIZE_AREA = 500

# Font. Not all fonts are supported
# Check OpenCV documentation
FONT = cv.FONT_HERSHEY_SIMPLEX

# Connect to camera
# If you have more than one camera connected
# Change 0 to 1 to choose second camera on so on
cap = cv.VideoCapture(0)
# Resize capture
cap.set(3, WIDTH)  # 3 =  CV_CAP_PROP_FRAME_WIDTH (Width of the frames in the video stream)
cap.set(4, HEIGHT) # 4 =  CV_CAP_PROP_FRAME_HEIGHT (Height of the frames in the video stream) 

# Create a window for sliders and frames
cv.namedWindow("Tracking", cv.WINDOW_FULLSCREEN)

# Real width of your object
REAL_WIDTH = 5

# Focal length of your camera
# Focal length = (Width in pixels *  Distance to object) / Width of an object
FOCAL_LENGTH = 832

# Then
# Distance to object = Focal length * Width of an object / Width in pixels
def distance(pixel_width, real_width, focal_length):
	return round(focal_length * real_width / pixel_width)

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

			original[:75, :255].fill(0)
			width_str = "Width is: " + str(w) + " px"

			cv.putText(original, width_str, (10,30), FONT, 0.7, (255,255,255), 1)

			dist_predict = distance(w,REAL_WIDTH, FOCAL_LENGTH)

			dist_str = "Distance is: " + str(dist_predict) + " cm"
			cv.putText(original, dist_str, (10, 60), FONT, 0.7, (255,255,255), 1)

			cv.rectangle(original, (x,y), (x+w,y+h), (0,255,0), 1)
			# Find center of a bounding rectangle
			center = (int(x+w/2), int(y+h/2))
			cv.circle(original, (center[0], center[1]), 3, (0,0,255), -1)
			# Calculate the x-center of a frame
			xc = int(original.shape[1] / 2)

			cv.line(original, (xc+TOLERANCE, 0), (xc+TOLERANCE, original.shape[0]), (0, 255, 255), 1)
			cv.line(original, (xc-TOLERANCE, 0), (xc-TOLERANCE, original.shape[0]), (0, 255, 255), 1)

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
		
cap.release()
cv.destroyAllWindows()					
