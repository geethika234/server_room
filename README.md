#Server-temp

## About

This system uses Computer Vision to detect the temperature reading from the display and a onboard temperature sensor and sends out alerts accordingly. It also records sound using microphone and tries to find out what noise it is wether it is humans,rebbot,normal or door being opened. This repository is where you can find the code that does the same.

### Requirements:
* Python 3.x
* Installing OpenCV on Raspberry Pi:
    - Refer to [this guide](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi), if necessary, to install OpenCV on your Pi.
* lm35 temperature sensor
* mcp3008(ADC)
* microphone with usb jack
* Installing Librosa on Raspberry Pi:
     - One has to install librosa by first installing berryconda and then installing librosa by command 'conda install -c conda-forge librosa'
### Seting up
* connect picam to camera slot on raspberry pi
* setting up temperature sensor 
      - Refer to [this guide](https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008) to set up temperature sensor and mcp3008 then copy tempsens code into examples folder of mcp3008 which you you just downloded
* connect microphone to one of the jacks of raspberry pi

### Getting Started
    
* __*Accessing the Raspberry Pi camera with Python and OpenCV*__:
	A picture of the temperature display is to be taken to be processed. A picture is taken every 10 mins by setting up a cron job.
* __*Accessing the temperature sensor*__:
        The value of temperature sensor is read every 10 mins
* __*Accessing the microphone*__:
        Sound is recorded for 10 seconds every 2 minutes and it's decibel level is evaluated and then find out what kind of that was.   

A sample image of the display: 
![Temp display](/images/image.jpg)

* __*Detecting the temperature on display reading*__:
	The temperature reading is displayed as seven segment digits. The steps to detect what digit it reads are as follows:
	- *Detecting the bright spots in the image*: Thresholding operations followed by dilation, erosion and other preprocessing functions returns an image with only the digits displayed highlighted.
	- *Extracting the digit ROI*: Contours that are large enough to be a digit(the appropriate width and height constraints requires a few rounds of trial and error) in the image is taken as a digit ROI. A contour is simply a curve joining all the continuous points (along the boundary), having same color or intensity.
	- *Identify the digits*: Recognizing the actual digits with OpenCV will involve dividing the digit ROI into seven segments. From there, pixel counting on the thresholded image is applied to determine if a given segment is “on” or “off”.

* __*Detecting the temperature using lm35 sensor*__:
        The value of sensor is read using tempsens code and is converted into temperature in degrees by multiplying it with a constant(28/100) and the obtained temperature is pushed into a text file which is later read in main.py file.
 
* __*Recording sound and finding decibel value of the sound*__:
	The sound is recorded using microphone with the command 'arecord -D plughw:1,0 -d 10 test.wav' and it's decibel value can be found using the code predict.py.

* __*Classifying sound into it's particular class*__:
	A machine learning technique called svm is used to classify sounds first one has to leave the microphone recording for 20 mins to 30 mins and later break these into smaller chunks of 10 seconds to obtain the test cases then we have to train the model on the laptop using train.py and deploy it on pi using scp protocol.
  
* __*Register*__:
	A site for users to register by providing a temperature threshold and email/phone number to receive alerts is up and running at [this site](https://roomserver.github.io/server/)
    
Users can opt-out from or resume receiving notifications via sending a mail with a specific subject and keyword by clicking on the link available on the site. Python's `imaplib` is used to read these received mails.
The database of users can be updated by running [getsheetdata.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/getsheetdata.py). Google Drive and Sheets API and Python's `gspread` library is used to implement this. References to this is linked down below. The status of the user's notification preference( active or inactive) is also checked and updated in the process.

Full code on Github: [getsheetdata.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/getsheetdata.py), [receive_mail.py](https://github.com/shwetha1607/Server-temp/blob/Version-1.1/receive_mail.py)

* __*Mailing service for sending out alerts*__: 
	Python's `smtplib` and `email` libraries are used for sending an email alert along with the image taken as an attachment, as and when the temperature detected exceeds the given acceptable range.

* __*SMS alerts*__:
	[TextLocal](https://www.textlocal.in/) is the SMS platform used to send out alerts via text messages programmatically. A SMS-bundle is purchased that provides a set of SMS credits that can be used to send messages(whose format follows a registered template created for the need) to any mobile number 24/7. Their [documentation](https://api.textlocal.in/docs/) provides the details and requirements to do so.
	
* __*Weekly mail*__:
	Every week once a mail is sent out showing the status of the server room 

### Scheduling tasks

To automate the tasks described above crontab is used. It periodically runs the jobs scheduled to it. The jobs basically are making the files in script_files folder run according to the frequency in which we want them to. The instructions for this model are in cron.txt file.



### References

* [Accessing Picamera with OpenCV and python](https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)
* [Recognizing digits](https://www.pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/)
* [Google Spreadsheets and Python](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
* [Python's imaplib](https://docs.python.org/3/library/imaplib.html)
* [Python's smtplib](https://docs.python.org/3/library/smtplib.html)
* [Python's email](https://docs.python.org/3/library/email.examples.html)
