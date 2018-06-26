import time
import RPi.GPIO as GPIO

M1_FORWARD_PIN = 26
M1_BACKWARD_PIN = 20

M2_FORWARD_PIN = 23
M2_BACKWARD_PIN = 24

def motor_setup():
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setup(M1_FORWARD_PIN, GPIO.OUT)
	GPIO.setup(M1_BACKWARD_PIN, GPIO.OUT)
	
	GPIO.setup(M2_FORWARD_PIN, GPIO.OUT)
	GPIO.setup(M2_BACKWARD_PIN, GPIO.OUT)

	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

def forward(t):
	GPIO.output(M1_FORWARD_PIN, GPIO.HIGH)
	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.HIGH)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

	time.sleep(t)	

	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)


def backward(t):
	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M1_BACKWARD_PIN, GPIO.HIGH)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.HIGH)

	time.sleep(t)	

	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)	

def turn_left(t):	
	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M1_BACKWARD_PIN, GPIO.HIGH)
	GPIO.output(M2_FORWARD_PIN, GPIO.HIGH)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

	time.sleep(t)	

	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)

def left(t):	
	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.HIGH)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

	time.sleep(t)	

	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)	
	
def turn_right(t):	
	GPIO.output(M1_FORWARD_PIN, GPIO.HIGH)
	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.HIGH)

	time.sleep(t)	

	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

def right(t):	
	GPIO.output(M1_FORWARD_PIN, GPIO.HIGH)
	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

	time.sleep(t)	

	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)

def stop():
	GPIO.output(M1_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M1_BACKWARD_PIN, GPIO.LOW)
	GPIO.output(M2_FORWARD_PIN, GPIO.LOW)
	GPIO.output(M2_BACKWARD_PIN, GPIO.LOW)			

def main():
	GPIO.cleanup()


if __name__ == '__main__':
		main()	