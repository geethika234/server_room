#!/bin/bash

source /home/pi/.profile
workon cv

python3 /home/pi/Detect_Notify/predict.py
