#!/bin/bash

source /home/pi/.profile
workon cv
cd /home/pi/Detect_Notify/
python /home/pi/Detect_Notify/everyweek.py
rm /home/pi/Detect_Notify/data.csv

