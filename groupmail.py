# Python code to illustrate Sending mail  
# to multiple users  
# from your Gmail account   
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
  
# list of email_id to send the mail 
def group(li,mess,Subject):
  
	for i in range(len(li)): 
		s = smtplib.SMTP('smtp.gmail.com', 'portno') 
		s.starttls() 
		s.login("username", "password") 
		message = mess
		Mail_Body = MIMEMultipart()
		Mail_Body['Subject'] = Subject
		Mail_Msg = MIMEText(message)
		Mail_Body.attach(Mail_Msg)
		s.sendmail("sender_email_id", li[i], Mail_Body.as_string()) 
		s.quit() 
