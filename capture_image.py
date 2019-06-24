from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
rawCapture = PiRGBArray(camera)

time.sleep(2.0)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

at_time = time.localtime()
time_str = time.strftime("%d-%m-%Y-%H:%M:%S", at_time)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.blur(gray, (5, 5))
#print(cv2.mean(blur))
if cv2.mean(blur)[0] < 3.0:
	# dark
	image_filename ="/home/pi/Pictures/server/dark/"+time_str+".jpg"
	cv2.imwrite(image_filename, image)
else:
	# lights on
	pass
