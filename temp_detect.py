import cv2
import numpy as np
import imutils
from imutils import contours
img_path = 'Image.jpg'
fr=99
DIGITS_LOOKUP = {
        (1, 1, 1, 0, 1, 1, 1): 0,
        (0, 0, 1, 0, 0, 1, 0): 1,
        (1, 0, 1, 1, 1, 0, 1): 2,
        (1, 0, 1, 1, 0, 1, 1): 3,
        (0, 1, 1, 1, 0, 1, 0): 4,
        (1, 1, 0, 1, 0, 1, 1): 5,
        (1, 1, 0, 1, 1, 1, 1): 6,
        (1, 0, 1, 0, 0, 1, 0): 7,
        (1, 1, 1, 1, 1, 1, 1): 8,
        (1, 1, 1, 1, 0, 1, 1): 9,
    }


class TempDetect:

    def __init__(self):

        # Load the image
        self.image = cv2.imread(img_path)

    def pre_processing(self, iteration_val,th):

        # Crop the image
        (h, w) = self.image.shape[:2]
        #print(self.image.shape)
        center = (w / 2, h / 2)
        #print(center)
        self.image = self.image[40:400, 150:600]
        cv2.imshow('image',self.image)

         
        self.image = imutils.resize(self.image, width = 950)

        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Convert pixels >110 to white
        thresh = cv2.threshold(gray, th, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=iteration_val)
        thresh = cv2.erode(thresh, None, iterations=1)

        blurred = cv2.GaussianBlur(thresh, (11, 11), 0)

        thresh = cv2.threshold(blurred, th, 255, cv2.THRESH_BINARY)[1]
        return thresh


    def find_contours(self, thresh):

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        digitCnts = []

        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            #print(x, y, w, h)
            #Scv2.rectangle(thresh, (x, y), (x+w, y+h), (255, 255, 255), 1)


            # if the contour is sufficiently large, it must be a digit
            # first condition for digit 1
            if (4 <= w <= 14) and (20 <= h <= 55):
                digitCnts.append(c)
            if (15 <= w <= 45) and (20 <= h <= 55):
                digitCnts.append(c)
                
        p=len(digitCnts)
        if p != 0:     
        	digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
        	fr=0
        else:
        	fr=1
        #print('len: ', len(digitCnts))
        return digitCnts

    def detect_digit(self, thresh, digitCnts):

        digits = []

        for c in digitCnts:
            (x, y, w, h) = cv2.boundingRect(c)
            #print(x, y, w, h)
            if (4 <= w <= 14) and (20 <= h <= 55):
                on = (0, 0, 1, 0, 0, 1, 0)
            else:
                roi = thresh[y:y+h, x:x+w]
                (roiH, roiW) = roi.shape

                (dW, dH) = (int(roiW * 0.3), int(roiH * 0.15))
                dHC = int(roiH * 0.05)
                dBR = int(roiW * 0.5)

                segments = [
                    ((dH, 0), (w-dH, dH)),  # top
                    ((0, dH), (dW, h // 2 - dHC)),  # top-left
                    ((w - dW, dH), (w, h // 2 - dHC)),  # top-right
                    ((dH, (h // 2)-dHC ), (w-dH, (h // 2)+dHC)),  # center
                    ((0, h // 2 + dHC), (dW, h - dH)),  # bottom-left
                    ((w - dBR, h // 2 + dHC), (w, h - dH)),  # bottom-right
                    ((dH, h - dH), (w-dH, h))  # bottom
                ]

                on = [0] * len(segments)

                for (i, ((xs, ys), (xf, yf))) in enumerate(segments):

                    segRoi = roi[ys:yf, xs:xf]
                    no_of_pixels = cv2.countNonZero(segRoi)
                    area = (xf - xs) * (yf - ys)

                    if no_of_pixels / float(area) >= 0.5:
                        on[i] = 1

                    #print(on)

            digit = DIGITS_LOOKUP.get(tuple(on), -1)
            digits.append(digit)

        return digits

    def final_call(self, iterval):
        thresh = self.pre_processing(iteration_val=iterval,th=120)
        digitCnts = self.find_contours(thresh)
        digits = self.detect_digit(thresh, digitCnts)
        if len(digitCnts)<2 or -1 in digits or fr==1:
        	self.image = cv2.imread(img_path)
        	print("1")
        	thresh = self.pre_processing(iteration_val=iterval,th=110)
        	digitCnts = self.find_contours(thresh)
        	digits = self.detect_digit(thresh, digitCnts)
        	if len(digitCnts)<2 or -1 in digits or fr==1:
        		self.image = cv2.imread(img_path)
        		print("hi")
        		thresh = self.pre_processing(iteration_val=iterval,th=105)
        		digitCnts = self.find_contours(thresh)
        		digits = self.detect_digit(thresh, digitCnts)
        		if len(digitCnts)<2 or -1 in digits or fr==1:
        			self.image = cv2.imread(img_path)
        			print("hi")
        			thresh = self.pre_processing(iteration_val=iterval,th=100)
        			digitCnts = self.find_contours(thresh)
        			digits = self.detect_digit(thresh, digitCnts)
        			if len(digitCnts)<2 or -1 in digits or fr==1:
        				self.image = cv2.imread(img_path)
        				print("hi")
        				thresh = self.pre_processing(iteration_val=iterval,th=95)
        				digitCnts = self.find_contours(thresh)
        				digits = self.detect_digit(thresh, digitCnts)
        				if len(digitCnts)<2 or -1 in digits or fr==1:
        					self.image = cv2.imread(img_path)
        					print("hi")
        					thresh = self.pre_processing(iteration_val=iterval,th=91)
        					digitCnts = self.find_contours(thresh)
        					digits = self.detect_digit(thresh, digitCnts)
        					if len(digitCnts)<2 or -1 in digits or fr==1:
        						self.image = cv2.imread(img_path)
        						print("hi")
        						thresh = self.pre_processing(iteration_val=iterval,th=85)
        						digitCnts = self.find_contours(thresh)
        						digits = self.detect_digit(thresh, digitCnts)
        						if len(digitCnts)<2 or -1 in digits or fr==1:
        							self.image = cv2.imread(img_path)
        							print("hi")
        							thresh = self.pre_processing(iteration_val=iterval,th=77)
        							digitCnts = self.find_contours(thresh)
        							digits = self.detect_digit(thresh, digitCnts)
        			
        			
        			
        return(digits)

ob = TempDetect()
ob.final_call(2)




