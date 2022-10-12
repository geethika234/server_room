x=list()
y1=list()
import numpy as np
import librosa
import os
import math
from sklearn.svm import SVC # "Support Vector Classifier"
from sklearn.metrics import accuracy_score
import pickle
Dataset = 'path/to/Normalrunning'
for filename in os.listdir(Dataset):
    if filename.endswith(".wav"):
        try:
            x1=list()
            y, sr = librosa.load(Dataset+"/"+filename)
            hop_length = 512
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
            mfcc_delta = librosa.feature.delta(mfcc)
            beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),beat_frames)
            chromagram = librosa.feature.chroma_cqt(y=y_harmonic,sr=sr)
            beat_chroma = librosa.util.sync(chromagram,beat_frames,aggregate=np.median)
            beat_features = np.vstack([beat_chroma, beat_mfcc_delta])
            x1.append(tempo)
            if not math.isnan(np.average(mfcc)):
                x1.append(np.average(mfcc))
            else:
                x1.append(0)
            if not math.isnan(np.average(mfcc_delta)):
                x1.append(np.average(mfcc_delta))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_mfcc_delta)):
                x1.append(np.average(beat_mfcc_delta))
            else:
                x1.append(0)
            if not math.isnan(np.average(chromagram)):
                x1.append(np.average(chromagram))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_chroma)):
                x1.append(np.average(beat_chroma))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_features)):
                x1.append(np.average(beat_features))
            else:
                x1.append(0)
            x.append(x1)
            y1.append(0)
        except:
                print(filename)       
   
Dataset = 'path/to/HumanVoice'
for filename in os.listdir(Dataset):
    if filename.endswith(".wav"):
        try:
            x1=[]
            y, sr = librosa.load(Dataset+"/"+filename)
            hop_length = 512
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
            mfcc_delta = librosa.feature.delta(mfcc)
            beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),beat_frames)
            chromagram = librosa.feature.chroma_cqt(y=y_harmonic,sr=sr)
            beat_chroma = librosa.util.sync(chromagram,beat_frames,aggregate=np.median)
            beat_features = np.vstack([beat_chroma, beat_mfcc_delta])
            x1.append(tempo)
            if not math.isnan(np.average(mfcc)):
                x1.append(np.average(mfcc))
            else:
                x1.append(0)
            if not math.isnan(np.average(mfcc_delta)):
                x1.append(np.average(mfcc_delta))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_mfcc_delta)):
                x1.append(np.average(beat_mfcc_delta))
            else:
                x1.append(0)
            if not math.isnan(np.average(chromagram)):
                x1.append(np.average(chromagram))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_chroma)):
                x1.append(np.average(beat_chroma))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_features)):
                x1.append(np.average(beat_features))
            else:
                x1.append(0)
             x.append(x1)
             y1.append(1)
        except:
                print(filename)
   
   
       
       
Dataset = 'path/to/DoorOpening'
for filename in os.listdir(Dataset):
    if filename.endswith(".wav"):
        try:
            x1=[]
            y, sr = librosa.load(Dataset+"/"+filename)
            hop_length = 512
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=hop_length, n_mfcc=13)
            mfcc_delta = librosa.feature.delta(mfcc)
            beat_mfcc_delta = librosa.util.sync(np.vstack([mfcc, mfcc_delta]),beat_frames)
            chromagram = librosa.feature.chroma_cqt(y=y_harmonic,sr=sr)
            beat_chroma = librosa.util.sync(chromagram,beat_frames,aggregate=np.median)
            beat_features = np.vstack([beat_chroma, beat_mfcc_delta])
            x1.append(tempo)
            if not math.isnan(np.average(mfcc)):
                x1.append(np.average(mfcc))
            else:
                x1.append(0)
            if not math.isnan(np.average(mfcc_delta)):
                x1.append(np.average(mfcc_delta))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_mfcc_delta)):
                x1.append(np.average(beat_mfcc_delta))
            else:
                x1.append(0)
            if not math.isnan(np.average(chromagram)):
                x1.append(np.average(chromagram))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_chroma)):
                x1.append(np.average(beat_chroma))
            else:
                x1.append(0)
            if not math.isnan(np.average(beat_features)):
                x1.append(np.average(beat_features))
            else:
                x1.append(0)
            x.append(x1)
            y1.append(2)
        except:
                print(filename)
   
   
       
       
             
print(x)
print(y1)  
    
 
clf = SVC(kernel='linear')
 
# fitting x samples and y classes
clf.fit(x, y1) 
s = pickle.dumps(clf)   
predicted = clf.predict(x)
# get the accuracy
print(predicted)
print(accuracy_score(y1, predicted)) 
dbfile = open('predict', 'ab')
# source, destination
pickle.dump(s, dbfile)                     
dbfile.close()
