import os
import sys
import pickle
from temp_detect import TempDetect
from send_sms import SendSMS
import groupmail as gmi
import groupnorm as gm
import csv
import time


class Driver():
	def __init__(self):
		dictfile = open('contacts_info.txt', 'rb')
		self.contacts_dict = pickle.load(dictfile)
		dictfile.close()
		self.smsobj = SendSMS()
	def get_image(self):
		latest_file = '/home/pi/Pictures/server/image.jpg'
		return latest_file

	def detect_digit(self):
		subject = 'Temperature Alert'
		negmsg = 'Unable to detect successfully. Detects: '
		alertmsg1 = 'Temperature beyond acceptable range. The display reads : '
		alertmsg2 = 'Temperature beyond acceptable range. The sensor reads : '
		add = ' and sensor reads: '
		img_path = self.get_image()
		tobj = TempDetect(img_path=img_path)
		digits = []
		try:
			# First attempt to detect. cv2.dilate() value = 2
			digits = tobj.final_call(iterval=2)
			# digits2 = digits[:2]
			digits_str = ''.join(str(x) for x in digits)
			self.disp=digits_str
			# Unable to map to a digit (returns -1) or detects no digit
			if -1 in digits or len(digits) < 2 or len(digits) > 2:
				message = negmsg+(digits_str[:3])
				gmi.group(['patchavageethika@gmail.com','butyg333@gmail.com'], message, subject)
		except Exception as exception:
			msg = 'ERROR: ' + type(exception).__name__ + str(exception)
			gmi.group(['patchavageethika@gmail.com','butyg333@gmail.com'], message, subject)
			
			message = alertmsg1+(digits_str[:3]) + add+str(sens)
			li = []
		for key in self.contacts_dict:
			# print(key)
			if self.contacts_dict[key]['status'] != 'Inactive':
				if (not (int(self.contacts_dict[key]['mint']) <= int(digits_str) <= int(self.contacts_dict[key]['maxt']))) or (not (int(self.contacts_dict[key]['mint']) <= sens <= int(self.contacts_dict[key]['maxt']))):
					# print("mail sent")
					li.append(self.contacts_dict[key]['mailid'])
					if self.contacts_dict[key]['mnum'] != '':
						elf.smsobj.sendSMS(message, self.contacts_dict[key]['mnum'])
			gmi.group(li, message, subject)
			
	def move_to_csv(self):
			t=time.localtime()
			row=[str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"/"+str(t.tm_hour)+"-"+str(t.tm_min),self.disp,str(self.sensor)]
			with open('data.csv', 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(row)
			csvFile.close()


mainobj = Driver()
mainobj.detect_digit()
mainobj.move_to_csv()
