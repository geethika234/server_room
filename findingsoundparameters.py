import csv
import time
import math
import statistics
from scipy.io import wavfile
import numpy as np
import pickle
#import numba
import librosa
p = []
x1 = []
x = []
filename="test.wav"
try:
	x1=list()
	y, sr = librosa.load("test.wav")
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
	p.append(x1)
	print(x1)
	f = ("ana2.txt","wb")
	pickle.dump(p,f)
	f.close()
except:

       f = ("ana2.txt","wb")
       g=0
       pickle.dump(g,f)
       f.close()
