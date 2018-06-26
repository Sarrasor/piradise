import cv2 as cv
import numpy as np

text= "No button was pressed"

# Create a font
font = cv.FONT_HERSHEY_SIMPLEX

while True:
	# Create a window
	img = np.zeros((150, 450))
	img.fill(255)
	cv.namedWindow("Key values", cv.WINDOW_FULLSCREEN)
	# Update text
	cv.putText(img, text, (10,30), font, 1, (0, 0, 0), 1)
	cv.putText(img, "Press Q to exit", (10,80), font, 1, (0, 0, 0), 1)
	cv.putText(img, "(Q value is 113)", (10,130), font, 1, (0, 0, 0), 1)	
	
	cv.imshow("Key values", img)

	# Wait for a key
	key = cv.waitKey(0)

	# Q key to exit
	if key == 113:    
		break
	# Normally -1 returned,so don't print it	
	elif key == -1:  
		continue       
	# Update key value 
	else:
		text = "This button's code: " + str(key)

cv.destroyAllWindows()				