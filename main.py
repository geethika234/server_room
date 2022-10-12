import os
import sys
import pickle
from temp_detect import TempDetect
from send_sms import SendSMS
import groupmail as gm
import groupmailimage as gmi
import csv
import time
import math
import statistics
from scipy.io import wavfile


class Driver():
	def __init__(self):
		dictfile = open('contacts_info.txt', 'rb')
		self.contacts_dict = pickle.load(dictfile)
		dictfile.close()
		self.smsobj = SendSMS()

	def detect_digit(self):
		subject = 'Temperature Alert'
		negmsg = 'Unable to detect successfully. Detects: '
		alertmsg1 = 'Temperature beyond acceptable range. The display reads : '
		alertmsg2 = 'Temperature beyond acceptable range. The sensor reads : '
		add = ' and sensor reads: '
		#img_path = self.get_image()
		#print(img_path)
		tobj = TempDetect()
		digits = []
		l = 0
		r = 0
		try:
			# First attempt to detect. cv2.dilate() value = 2
			#print("hey")
			digits = tobj.final_call(iterval=2)
			# digits2 = digits[:2]
			digits_str = ''.join(str(x) for x in digits)
			self.disp=digits_str
			print(digits)
			# Unable to map to a digit (returns -1) or detects no digit
			if -1 in digits or len(digits) < 2 or len(digits) > 2:
				message = negmsg+(digits_str[:3])
				self.disp='-666'
				gmi.group(['your email'], message, subject)
				r = 1
		except Exception as exception:
			self.disp='-666'
			msg = 'ERROR: ' + type(exception).__name__ + str(exception)
			gmi.group(['your email'], msg, subject)
			r = 1
			
		try:
			dictfile = open('server.txt', 'rb')
			sens = pickle.load(dictfile)
			dictfile.close()
			print(sens)
			self.sensor=sens
			if sens < 0 or sens > 30:
				self.sensor='-666'
				message = negmsg+str(sens)
				gm.group(['your email'], message, subject)
				l = 1
				
		except Exception as exception:
			# print("i")
			self.sensor='-666'
			msg = 'ERROR: ' + type(exception).__name__ + str(exception)
			gm.group(['your email'], msg, subject)
			l = 1
			
		if r == 1 and l == 1:
			print("everything wrong")
		elif r == 0 and l == 0:
			message = alertmsg1+(digits_str[:3]) + add+str(sens)
			li = []
			for key in self.contacts_dict:
				# print(key)
				if self.contacts_dict[key]['status'] != 'Inactive':
					if (not (int(self.contacts_dict[key]['mint']) <= int(digits_str) <= int(self.contacts_dict[key]['maxt']))) or (not (int(self.contacts_dict[key]['mint']) <= sens <= int(self.contacts_dict[key]['maxt']))):
						# print("mail sent")
						li.append(self.contacts_dict[key]['mailid'])
						if self.contacts_dict[key]['mnum'] != '':
							self.smsobj.sendSMS(message, self.contacts_dict[key]['mnum'])
			gmi.group(li, message, subject)
			
		elif r == 0:
			message = alertmsg1 + (digits_str[:3])
			li = []
			for key in self.contacts_dict:
				# print(key)
				if self.contacts_dict[key]['status'] != 'Inactive':
					if (not (int(self.contacts_dict[key]['mint']) <= int(digits_str) <= int(self.contacts_dict[key]['maxt']))):
						# print("mail sent")
						li.append(self.contacts_dict[key]['mailid'])
						if self.contacts_dict[key]['mnum'] != '':
							self.smsobj.sendSMS(message, self.contacts_dict[key]['mnum'])
			gmi.group(li, message, subject)
			
		else:
			message = alertmsg2+str(sens)
			li = []
			for key in self.contacts_dict:
				# print(key)
				if self.contacts_dict[key]['status'] != 'Inactive':
					if (not (int(self.contacts_dict[key]['mint']) <= sens <= int(self.contacts_dict[key]['maxt']))):
						# print("mail sent")
						li.append(self.contacts_dict[key]['mailid'])
						if self.contacts_dict[key]['mnum'] != '':
							self.smsobj.sendSMS(message, self.contacts_dict[key]['mnum'])
			gmi.group(li, message, subject)
            
		
	def move_to_csv(self):
			t=time.localtime()
			#print("hello")
			row=[str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"/"+str(t.tm_hour)+"-"+str(t.tm_min),self.disp,str(self.sensor),str(k)]
			with open('data.csv', 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(row)
			csvFile.close()


mainobj = Driver()
mainobj.detect_digit()
mainobj.move_to_csv()
