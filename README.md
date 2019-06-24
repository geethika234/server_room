# Server-temp

## About

This system uses Computer Vision to detect the temperature reading from the display and also reads temperature from temperature sensor and sends out alerts accordingly. This repository is where you can find the code that does the same.

### Requirements:
* Python 3.x
* Installing OpenCV on Raspberry Pi:
    - Refer to [this guide](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi), if necessary, to install OpenCV on your Pi. Once insalled correctly, you should be able to import it as:
    ```python
    import cv2
    ```
* [requirements.txt]()
* MCP3008
* LM35 temperature sensor
* Bread Board and Jumper Wires

### Getting Started
    
* __*Accessing the Raspberry Pi camera with Python and OpenCV*__:
	A picture of the temperature display is to be taken to be processed. A picture is taken every 10 mins by setting up a cron job and this image is saved into a folder such that it contains last one week data.
    
###### Saving the image:
```python
# image is the opencv numpy array representation of the picture taken
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (5, 5))
cv2.imwrite('/home/pi/Pictures/server/image.jpg', image)
```

A sample image: 
![Temp display](image.jpg)


* __*Detecting the temperature reading*__:
	The temperature reading is displayed as seven segment digits. The steps to detect what digit it reads are as follows:
	- *Detecting the bright spots in the image*: Thresholding operations followed by dilation, erosion and other preprocessing functions returns an image with only the digits displayed highlighted.
	- *Extracting the digit ROI*: Contours that are large enough to be a digit(the appropriate width and height constraints requires a few rounds of trial and error) in the image is taken as a digit ROI. A contour is simply a curve joining all the continuous points (along the boundary), having same color or intensity.
	- *Identify the digits*: Recognizing the actual digits with OpenCV will involve dividing the digit ROI into seven segments. From there, pixel counting on the thresholded image is applied to determine if a given segment is “on” or “off”.

#### Temperature Sensor:
	Connections of lm35,mcp3008 and raspberry pi are:
    * MCP3008 VDD to Raspberry Pi 3.3V
    * MCP3008 VREF to Raspberry Pi 3.3V
    * MCP3008 AGND to Raspberry Pi GND
    * MCP3008 DGND to Raspberry Pi GND
    * MCP3008 CLK to Raspberry Pi SCLK
    * MCP3008 DOUT to Raspberry Pi MISO
    * MCP3008 DIN to Raspberry Pi MOSI
    * MCP3008 CS/SHDN to Raspberry Pi CE0
    * lm35 GND to Raspberry Pi GND	
    * lm35 vcc to Raspberry Pi 5v
    * lm35 middle pin to MCP3008 channel 1
    

#### Temperature sensor setup:
   	 Type the follwing commands in the terminal:
           git clone https://github.com/adafruit/Adafruit_Python_MCP3008.git
	       cd Adafruit_Python_MCP3008
	   sudo python setup.py install
     Now copy tempsens code into a file in folder examples and run that file to get the temperature and to store into a text file
	


* __*Register*__:
	A site for users to register by providing a temperature threshold and email/phone number to receive alerts is up and running at [this site](https://roomserver.github.io/server/)
    
Users can opt-out from or resume receiving notifications via sending a mail with a specific subject and keyword by clicking on the link available on the site. Python's `imaplib` is used to read these received mails.
The database of users can be updated by running the getsheetdata.py code give above. Google Drive and Sheets API and Python's `gspread` library is used to implement this. References to this is linked down below. The status of the user's notification preference( active or inactive) is also checked and updated in the process.


* __*Mailing service for sending out alerts*__: 
	Python's `smtplib` and `email` libraries are used for sending an email alert along with the image taken as an attachment, as and when the temperature detected exceeds the given acceptable range.

* __*SMS alerts*__:
	[TextLocal](https://www.textlocal.in/) is the SMS platform used to send out alerts via text messages programmatically. A SMS-bundle is purchased that provides a set of SMS credits that can be used to send messages(whose format follows a registered template created for the need) to any mobile number 24/7. Their [documentation](https://api.textlocal.in/docs/) provides the details and requirements to do so.

All the above metioned functionalities is encapsulated and run by the driver program: center.py

### Scheduling tasks

To automate taking a picture and processing the image to detect temperature reading followed by sending alerts if required, are scheduled to execute every 10 minutes using Cron. Cron is a tool for configuring scheduled tasks on Unix systems. It is used to schedule commands or scripts to run periodically and at fixed intervals. `final_execute.sh` is the shell script scheduled to run every 10 minutes.

###### final_execute.sh
```shell
!/bin/bash

source ~/.profile
workon cv
python /home/pi/pic.py
python /home/pi/Detect_Notify/center.py
```
###### final_execute_sensor.sh
```shell
!/bin/bash

source ~/.profile
workon cv
cd /home/pi/Adafruit_Python_MCP3008/examples
python /home/pi/Adafruit_Python_MCP3008/examples/tempsens.py
```

### Feedback

For any feedback, queries, fill in this [form](https://roomserver.github.io/server/feedback.html).

### References

* [Accessing Picamera with OpenCV and python](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)
* [Recognizing digits](https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/)
* [Google Spreadsheets and Python](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
* [Python's imaplib](https://docs.python.org/3/library/imaplib.html)
* [Python's smtplib](https://docs.python.org/3/library/smtplib.html)
* [Python's email](https://docs.python.org/3/library/email.examples.html)
* [Temperature sensor connections](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008)
