#!/bin/bash

source /home/pi/.profile
workon cv
cd /home/pi/Detect_Notify/
python /home/pi/Detect_Notify/getsheetdata.py
