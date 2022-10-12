import urllib.request
import urllib.parse


class SendSMS:
    def __init__(self):
        self.apiKey = 'apikey'
        self.sender = 'senderid'


    def sendSMS(self, message, number):
        number = '91'+number
        data = urllib.parse.urlencode({
            'apikey': self.apiKey,
            'numbers': number,
            'message': message,
            'sender': self.sender
        })
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()

