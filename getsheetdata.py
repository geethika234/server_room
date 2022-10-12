import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pickle
from receive_mail import ReceiveEmail

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
sheet = client.open("Temperature alerts (Responses)").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()

info = sheet.get_all_values()

contacts_dict = dict()
for i in range(1, len(info)):
	if info[i][8] == '':
		sheet.update_cell(i+1, 9, 'Active')

info = sheet.get_all_values()
for i in range(1, len(info)):
	name = info[i][1] + info[i][2]
	contacts_dict[name] = {'rnum': info[i][3], 'mint': info[i][4], 'maxt': info[i][5], 'mailid': info[i][6], 'mnum': info[i][7], 'status': info[i][8]}

mobj = ReceiveEmail()
mobj.receiveMail()

for name, idict in contacts_dict.items():
	if idict['mailid'] in mobj.from_addr:
		idict['status'] = 'Inactive'
	if idict['mailid'] in mobj.re_addr:
		idict['status'] = 'Active'


#Save contacts in the form of the dictionary where first_name+last_name acts as the key
dictfile = open('contacts_info.txt', 'wb')
pickle.dump(contacts_dict, dictfile)
dictfile.close()



