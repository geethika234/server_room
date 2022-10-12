import email
import imaplib

class ReceiveEmail:
	def __init__(self):
		self.obj = Email()
		self.mailID = "username"
		self.password = "password"
		self.M = imaplib.IMAP4_SSL('imap.gmail.com')
		self.from_addr = []
		self.re_addr = []

	def processMail(self):
		status, data = self.M.search(None, '(UNSEEN)')
		if status != 'OK':
			print("No messages found")
			return

		#print('Data:', data)
		#print(data[0].split())
		for num in data[0].split():
			status, data = self.M.fetch(num, '(RFC822)')
			if status != 'OK':
				print("Error reading message", num)
				return

			msg = email.message_from_bytes(data[0][1])
			#print ('Message %s: %s' % (num, msg['Subject']))
			if msg['Subject'] == 'Stop alerts':
				for part in msg.walk():
					if part.get_content_type() == 'text/plain':
						message_received = part.get_payload()
						if message_received[:4] == 'STOP':
							self.from_addr.append((email.utils.parseaddr(msg['From']))[1])
						if message_received[:7] == 'RESTART':
							self.re_addr.append((email.utils.parseaddr(msg['From']))[1])
				typ, data = self.M.store(num,'+FLAGS','\\Seen')

		return

	def receiveMail(self):
		try:
			self.M.login(self.mailID, self.password)
		except imaplib.IMAP4.error:
			print("Error logging in")
			exit()

		status, data = self.M.select('INBOX')
		if status == 'OK':
			#print("Processing mail")
			self.processMail()
			self.M.close()
		else:
			print('Nothing returned')
		self.M.logout()
