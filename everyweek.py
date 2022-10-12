import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import pickle
import matplotlib.pyplot as plt
import csv
x = []
y = []
with open('data.csv','r') as csvfile:
     plots = csv.reader(csvfile, delimiter=',')
     for row in plots:
         x.append(float(row[0]))
         y.append(float(row[2]))
plt.plot(x,y, label='Time vs display')
plt.savefig('Timevsdisplay.jpg')
plt.clf()
x = []
y = []
with open('data.csv','r') as csvfile:
     plots = csv.reader(csvfile, delimiter=',')
     for row in plots:
         x.append(float(row[0]))
         y.append(float(row[3]))
plt.plot(x,y, label='Time vs sensor')
plt.savefig('Timevssensor.jpg')
plt.clf()
x = []
y = []
with open('deci.csv','r') as csvfile:
     plots = csv.reader(csvfile, delimiter=',')
     for row in plots:
         x.append(float(row[0]))
         y.append(float(row[3]))
plt.plot(x,y, label='Time vs decibel')
plt.savefig('Timevsdecibel.jpg')
plt.clf()
def group(li,mess,Subject):
        emailfrom = "roomserver.cds@gmail.com"
        for i in range(len(li)):
                emailto =li[i]
                fileToSend = ["data.csv","Timevsdisplay.jpg","Timevssensor.jpg","deci.csv","Timevsdecibel.jpg"]
                username = "roomserver.cds@gmail.com"
                password = "server209"
                print(li[i])
                msg = MIMEMultipart()
                msg["From"] = username
                msg["To"] = emailto
                msg["Subject"] = Subject
                for k in fileToSend:
                        ctype, encoding = mimetypes.guess_type(k)
                        if ctype is None or encoding is not None:
                                ctype = "application/octet-stream"
                        maintype, subtype = ctype.split("/", 1)
                        if maintype == "text":
                                fp = open(k)
                                # Note: we should handle calculating the charset
                                attachment = MIMEText(fp.read(), _subtype=subtype)
                                fp.close()
                        elif maintype == "image":
                                fp = open(k, "rb")
                                attachment = MIMEImage(fp.read(), _subtype=subtype)
                                fp.close()
                        elif maintype == "audio":
                                fp = open(k, "rb")
                                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                                fp.close()
                        else:
                                fp = open(k, "rb")
                                attachment = MIMEBase(maintype, subtype)
                                attachment.set_payload(fp.read())
                                fp.close()
                                encoders.encode_base64(attachment)
                        attachment.add_header("Content-Disposition", "attachment", filename=k)
                        msg.attach(attachment)
                server = smtplib.SMTP("smtp.gmail.com:587")
                server.starttls()
                server.login(username,password)
                server.sendmail(emailfrom, emailto, msg.as_string())
                server.quit()
dictfile = open('contacts_info.txt', 'rb')
contacts_dict = pickle.load(dictfile)
dictfile.close()
li = []
for key in contacts_dict:
        if contacts_dict[key]['status'] != 'Inactive':
                li.append(contacts_dict[key]['mailid'])
print("sent")
#print(li)
#group(['patchavageethika@gmail.com'],"last one week data","data")
group(li,"last one week data","data")


