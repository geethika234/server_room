import os
import sys
import shutil
import pickle
import glob
from temp_detect import TempDetect
from send_sms import SendSMS
from send_mail import SendEmail

class Driver():
	def __init__(self):
		dictfile = open('contacts_info.txt', 'rb')
		self.contacts_dict = pickle.load(dictfile)
		dictfile.close()
		self.smsobj = SendSMS()
		self.mailobj = SendEmail()

	def get_image(self):
		list_of_files = glob.glob('/home/pi/Pictures/server/dark/*')
		latest_file = max(list_of_files, key=os.path.getctime)
		return latest_file

	def detect_digit(self):
		subject = 'Temperature Alert'
		negmsg = 'Unable to detect successfully. Detects: '
		alertmsg = 'Temperature beyond acceptable range. The display reads: '
		img_path = self.get_image()
		tobj = TempDetect(img_path=img_path)
		digits = []

		try:
			# First attempt to detect. cv2.dilate() value = 1
			digits = tobj.final_call(iterval=1)
			digits_str = u'{}{}'.format(*digits)

			# Unable to map to a digit (returns -1)
			if -1 in digits:
				# Second attempt to detect. cv2.dilate() value = 2
				digits = tobj.final_call(iterval=2)
				digits_str = u'{}{}'.format(*digits)

				# Unable to detect second time
				if -1 in digits:
					for key in self.contacts_dict:
						self.mailobj.sendEmail(self.contacts_dict[key]['mailid'], subject, negmsg, img_path)
						self.smsobj.sendSMS(negmsg, self.contacts_dict[key]['mnum'])
					sys.exit()

				#Else, successfully detected (2nd attempt)
			#Else, successfully detected (1st attempt)

		# Unable to detect both the digits correctly
		except IndexError:
			digits = tobj.final_call(iterval=2)
			# Still unable to detect 2nd time (either -1 or misses one digit)
			if -1 in digits or len(digits)<2:
				for key in self.contacts_dict:
					self.mailobj.sendEmail(self.contacts_dict[key]['mailid'], subject, negmsg, img_path)
					if self.contacts_dict[key]['mnum'] != '':
						self.smsobj.sendSMS(negmsg, self.contacts_dict[key]['mnum'])


		digits2 = digits[:2]
		digits_str = ''.join(str(x) for x in digits2)

		for key in self.contacts_dict:
        	if not self.contacts_dict[key]['mint'] < digits_str < self.contacts_dict[key]['maxt']:
	            self.mailobj.sendEmail(self.contacts_dict[key]['mailid'], subject, alertmsg, moved_to)
	            if self.contacts_dict[key]['mnum'] != '':
					self.smsobj.sendSMS(alertmsg, self.contacts_dict[key]['mnum'])

			else:
				# Within the given range. Do nothing.
				pass



mainobj = Driver()
mainobj.detect_digit()