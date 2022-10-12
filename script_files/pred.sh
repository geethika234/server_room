#!/bin/bash 

cd /home/pi/Detect_Notify/
arecord -D plughw:1,0 -d 10 test.wav

cd /home/pi/Detect_Notify/
python3 /home/pi/Detect_Notify/findingsoundparameters.py








