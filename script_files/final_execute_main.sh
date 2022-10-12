#!/bin/bash

source /home/pi/.profile
workon cv
python /home/pi/stillpic.py
cd /home/pi/Detect_Notify/
arecord -D plughw:1,0 -d 3 test.wav
cp -b /home/pi/Detect_Notify/test.wav /home/pi/Pictures/"$(date +"%Y-%m-%d")"

cd /home/pi/Pictures/"$(date +"%Y-%m-%d")"
mv test.wav  "$(date +"%T")".wav
cd /home/pi/Detect_Notify/
python /home/pi/Detect_Notify/maino.py

