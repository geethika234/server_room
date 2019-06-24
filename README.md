# Server-temp

## About

This system uses Computer Vision to detect the temperature reading from the display and sends out alerts accordingly. This repository is where you can find the code that does the same.

### Requirements:
* Python 3.x
* Installing OpenCV on Raspberry Pi:
    - Refer to [this guide](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi), if necessary, to install OpenCV on your Pi. Once insalled correctly, you should be able to import it as:
    ```python
    import cv2
    ```
* [requirements.txt]()

### Getting Started
    
* __*Accessing the Raspberry Pi camera with Python and OpenCV*__:
	A picture of the temperature display is to be taken to be processed. A picture is taken every hour by setting up a cron job. This picture is saved to be processed only if the lights aren't turned on in the server room, i.e. only when the environment is dark.
    
###### Saving the image:
```python
# image is the opencv numpy array representation of the picture taken
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (5, 5))
if cv2.mean(blur)[0] < 3.0:
	cv2.imwrite('/home/pi/Pictures/server/image.jpg', image)
else:
	# Lights on
	pass
```

A sample image: 
![Temp display](/images/image.jpg)

Full Code on Github: [stillpic.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/stillpic.py)

* __*Detecting the temperature reading*__:
	The temperature reading is displayed as seven segment digits. The steps to detect what digit it reads are as follows:
	- *Detecting the bright spots in the image*: Thresholding operations followed by dilation, erosion and other preprocessing functions returns an image with only the digits displayed highlighted.
	- *Extracting the digit ROI*: Contours that are large enough to be a digit(the appropriate width and height constraints requires a few rounds of trial and error) in the image is taken as a digit ROI. A contour is simply a curve joining all the continuous points (along the boundary), having same color or intensity.
	- *Identify the digits*: Recognizing the actual digits with OpenCV will involve dividing the digit ROI into seven segments. From there, pixel counting on the thresholded image is applied to determine if a given segment is “on” or “off”.

###### Snippets of the code from temp_detect.py depicting above steps:

```python
# Detecting bright spots: Convert pixels >110 to white
thresh = cv2.threshold(image, 110, 255, cv2.THRESH_BINARY)[1]
```

```python
# Finding contours and extracting digit ROI
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
digitCnts = []
	
for c in cnts:
  # compute the bounding box of the contour
  (x, y, w, h) = cv2.boundingRect(c)
  # if the contour is sufficiently large, it must be a digit
  if (15 <= w <= 45) and (20 <= h <= 55):
      digitCnts.append(c)
```

```python
# Identify the digits
on = [0] * len(segments)

for (i, ((xs, ys), (xf, yf))) in enumerate(segments):
  segRoi = roi[ys:yf, xs:xf]  # Get segment ROI
  no_of_pixels = cv2.countNonZero(segRoi)
  area = (xf - xs) * (yf - ys)
  
  # If the number of white pixels in segment ROI is greater than 50%, the segment is active
  # If true, on[segment_num] = 1
  if no_of_pixels / float(area) >= 0.5:
      on[i] = 1

# digit has the number the seven segment display shows. 
# DIGITS_LOOKUP is a dictionary that maps a seven element tuple (on) to its digit value.
digit = DIGITS_LOOKUP.get(tuple(on), -1)
```
	
Full Code on Github: [temp_detect.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/temp_detect2.py)

* __*Register*__:
	A site for users to register by providing a temperature threshold and email/phone number to receive alerts is up and running at [this site](https://roomserver.github.io/Server-Temperature/)
    
Users can opt-out from or resume receiving notifications via sending a mail with a specific subject and keyword by clicking on the link available on the site. Python's `imaplib` is used to read these received mails.
The database of users can be updated by running [getsheetdata.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/getsheetdata.py). Google Drive and Sheets API and Python's `gspread` library is used to implement this. References to this is linked down below. The status of the user's notification preference( active or inactive) is also checked and updated in the process.

Full code on Github: [getsheetdata.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/getsheetdata.py), [receive_mail.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/receive_mail.py)

* __*Mailing service for sending out alerts*__: 
	Python's `smtplib` and `email` libraries are used for sending an email alert along with the image taken as an attachment, as and when the temperature detected exceeds the given acceptable range.

* __*SMS alerts*__:
	[TextLocal](https://www.textlocal.in/) is the SMS platform used to send out alerts via text messages programmatically. A SMS-bundle is purchased that provides a set of SMS credits that can be used to send messages(whose format follows a registered template created for the need) to any mobile number 24/7. Their [documentation](https://api.textlocal.in/docs/) provides the details and requirements to do so.
	
* The credentials for sending out mails and texts are saved as *config.py* in the following format:
```python
class TextLocal:
        def __init__(self):
                self.apiKey = 'api-key'
                self.senderID = 'Sender ID'              

class Email:
        def __init__(self):
                self.SMTP_SERVER = 'smtp.gmail.com'
                self.SMTP_PORT = 465
                self.FROM_ADD = 'user@gmail.com'
                self.USERNAME = 'user@gmail.com'
                self.PASSWORD = 'password'
```

All the above metioned functionalities is encapsulated and run by the driver program: [pidriver.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/pidriver.py)


### Scheduling tasks

To automate taking a picture and processing the image to detect temperature reading followed by sending alerts if required, are scheduled to execute every hour using Cron. Cron is a tool for configuring scheduled tasks on Unix systems. It is used to schedule commands or scripts to run periodically and at fixed intervals. `final_execute.sh` is the shell script scheduled to run every hour.

###### final_execute.sh
```shell
!/bin/bash

source ~/.profile
workon cv
python /home/pi/stillpic.py
python /home/pi/Detect_Notify/pidriver.py
```

### Feedback

For any feedback, queries, fill in this [form](https://docs.google.com/forms/d/e/1FAIpQLSd1Hi3Tuu2ZcA4oDTHY-hGVPQgglfqPrlwuhB64tccOtaXlug/viewform).

### References

* [Accessing Picamera with OpenCV and python](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)
* [Recognizing digits](https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/)
* [Google Spreadsheets and Python](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
* [Python's imaplib](https://docs.python.org/3/library/imaplib.html)
* [Python's smtplib](https://docs.python.org/3/library/smtplib.html)
* [Python's email](https://docs.python.org/3/library/email.examples.html)
