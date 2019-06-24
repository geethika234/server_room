import urllib.request
import urllib.parse
from config import TextLocal

class SendSMS:
	def __init__(self):
		self.smsObj = TextLocal()
		self.apiKey = self.smsObj.apiKey
		self.sender =self.smsObj.senderID
		self.group = self.smsObj.groupID

	def sendSMSG(self, message):
		data = urllib.parse.urlencode({
	    	'apikey': self.apiKey, 
	    	'group_id': self.group,
	    	'message': message, 
	    	'sender': self.sender
	    })
		data = data.encode('utf-8')
		print('Attempt to send')
		print(data)
		request = urllib.request.Request("https://api.textlocal.in/send/?")
		f = urllib.request.urlopen(request, data)
		fr = f.read()
		#print(fr)
		#return fr

	def sendSMS(self, message, number):
		numbers = '91'+number
		data = urllib.parse.urlencode({
	    	'apikey': self.apiKey, 
	    	'numbers': number,
	    	'message': message, 
	    	'sender': self.sender
	    })
		data = data.encode('utf-8')
		print('Attempt to send')
		print(data)
		request = urllib.request.Request("https://api.textlocal.in/send/?")
		f = urllib.request.urlopen(request, data)
		fr = f.read()


#obj = SendSMS()
#resp =obj.sendSMS('This is a test message template. 22')
#print(resp)