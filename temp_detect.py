import cv2
import numpy as np
import imutils
from imutils import contours

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

    def __init__(self, img_path):

        # Load the image
        self.image = cv2.imread(img_path)

    def pre_processing(self, iteration_val):

        # Crop the image
        self.image = self.image[100:380, 50:600]

        # Convert to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Convert pixels >110 to white
        thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=iteration_val)
        thresh = cv2.erode(thresh, None, iterations=1)

        return thresh

    def find_contours(self, thresh):

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        digitCnts = []

        for c in cnts:
            # compute the bounding box of the contour
            (x, y, w, h) = cv2.boundingRect(c)
            # print(x, y, w, h)

            cv2.rectangle(thresh, (x, y), (x+w, y+h), (255, 255, 255), 1)

            # if the contour is sufficiently large, it must be a digit
            # first condition for digit 1
            if (2 <= w <= 6) and (10 <= h <= 25):
                digitCnts.append(c)
            if (5 <= w <= 15) and (14 <= h <= 25):
                digitCnts.append(c)

        digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

        return digitCnts

    def detect_digit(self, thresh, digitCnts):

        digits = []

        for c in digitCnts:
            (x, y, w, h) = cv2.boundingRect(c)
            print(x, y, w, h)
            if (2 <= w <= 6) and (10 <= h <= 25):
                on = (0, 0, 1, 0, 0, 1, 0)
            else:
                roi = thresh[y+1:y+h, x:x+w]
                (roiH, roiW) = roi.shape
                # print(roiH, roiW)

                (dW, dH) = (int(roiW * 0.3), int(roiH * 0.1))
                dhb = int(roiH * 0.15)
                h = h - 1
                dHC = int(roiH * 0.08)

                segments = [
                    ((0, 0), (w, dH)),  # top
                    ((0, 0), (dW, h // 2)),  # top-left
                    ((w - dW, 0), (w, h // 2)),  # top-right
                    ((0, (h // 2) - dHC), (w, (h // 2) + dHC)),  # center
                    ((0, h // 2), (dW, h)),  # bottom-left
                    ((w - dW, h // 2), (w, h)),  # bottom-right
                    ((0, h - dhb), (w, h))  # bottom
                ]

                on = [0] * len(segments)

                for (i, ((xs, ys), (xf, yf))) in enumerate(segments):

                    segRoi = roi[ys:yf, xs:xf]
                    no_of_pixels = cv2.countNonZero(segRoi)
                    area = (xf - xs) * (yf - ys)

                    if no_of_pixels / float(area) >= 0.54:
                        on[i] = 1

                    # print(on)

            digit = DIGITS_LOOKUP.get(tuple(on), -1)
            digits.append(digit)

            #print(x,y,w,h)
            '''mod_image = self.image
            cv2.rectangle(mod_image.copy(), (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(mod_image.copy(), str(digit), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 1)'''

        return digits

    def final_call(self, iterval):
        thresh = self.pre_processing(iteration_val=iterval)
        digitCnts = self.find_contours(thresh)
        digits = self.detect_digit(thresh, digitCnts)
        return digits


