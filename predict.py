	
import pickle
import csv
import time 

f=open("file.out","r")
p=f.read()
if p==0:
	r=0
else:
	dbfile = open('predit', 'rb')
	db = pickle.load(dbfile)
	e = pickle.loads(db)
	r=e.predict(p)
if r==0:
	a='normal'
else:
	a='humans'

try:
	with open('deci.csv','r') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			x.append(str(row[0]))
		data=x[len(x)-1]
		print(data)

except:
	data=0
	print(data)
da=int(data)
t=time.localtime()
#print("hello")
try:
	sampFreq, snd = wavfile.read('test.wav')
	s1 = snd / (2.**15)
	l=math.sqrt(statistics.mean(s1**2))
	k=20*math.log(l,10)+122
	print(k)
except:
	k=-666
sampFreq, snd = wavfile.read('test.wav')
a='normal'
if a=='normal' and k>73.8023:
	a='reebot'
row=[str(da+1),a,str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+"/"+str(t.tm_hour)+"-"+str(t.tm_min),str(k)]
with open('deci.csv', 'a') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerow(row)
csvFile.close()
