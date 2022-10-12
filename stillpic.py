from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import cv2
import os


camera= PiCamera()
camera.resolution = (640, 480)
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(5)
camera.capture(rawCapture,format='bgr')
image = rawCapture.array
t = time.localtime()
at_time=str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"/"+str(t.tm_hour)+"-"+str(t.tm_min)
print(at_time)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (5, 5))
cv2.imwrite('/path/to/folder/image.jpg', image)
if t.tm_hour==0 and t.tm_min==0 or t.tm_min==1 or t.tm_min==2:
	os.system('./create_remove.sh') # a script file to create a new directory

os.system('./push.sh') # a script file to copy image to folder with time stamp
cv2.destroyAllWindows()

