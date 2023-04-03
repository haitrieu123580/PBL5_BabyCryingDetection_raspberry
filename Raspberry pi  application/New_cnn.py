
import os
import numpy as np
import threading
import pyaudio
import wave
import soundfile as sf
import time
import librosa
from keras.models import model_from_json
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import keras
from keras import backend as K
from keras.models import Sequential,model_from_json
from keras.layers import Conv2D,Conv1D,MaxPooling1D,GlobalAveragePooling1D,GlobalMaxPooling1D
from keras.layers import MaxPooling2D
from keras.layers import Flatten,Dropout
from keras import optimizers, callbacks
import numpy as np
from keras.layers import Dense,Activation
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from python_speech_features import logfbank
from scipy.signal import butter,lfilter,freqz
from tensorflow.keras.utils import img_to_array
from python_speech_features import mfcc
fs = 44100

# D:\\HK2-Năm 3\\PBL5\\Code\\Smart_cradle_system\\Baby Cry Detection\\Model Training\\cnn.json
with open('D:\\HK2-Năm 3\\PBL5\\Code\\Smart_cradle_system\\Baby Cry Detection\\Model Training\\cnn.json', 'r') as f:
    mymodel=model_from_json(f.read())

mymodel.load_weights("D:\\HK2-Năm 3\\PBL5\\Code\\Smart_cradle_system\\Baby Cry Detection\\Model Training\\cnn.h5")


def feature(soundfile):
    s,r=sf.read(soundfile)
    # s=butter_lowpass_filter(s,11025,44100,order=3)
    x=np.array_split(s,64)
    
    logg=np.zeros((64,12))
    for i in range(len(x)):

        m=np.mean(mfcc(x[i],r, numcep=12,nfft=2048),axis=0)
        logg[i,:]=m

    return logg  

def doafter5():
    l = None
    livesound = None
    l = pyaudio.PyAudio()
    record_second = 5
    CHANNELS = 2
    livesound = l.open(format=pyaudio.paInt16,
                 channels= CHANNELS,
                 rate=fs, input=True,frames_per_buffer=8192,input_device_index = 2
                 )
    livesound.start_stream() 
    Livesound = None
    li = []
    
    timeout = time.time()+20
    for f in range(0, int(fs/8192*record_second)):
        Livesound = livesound.read(8192)
        li.append(Livesound)
        
   
    waves = wave.open('rec.wav','w')
    waves.setnchannels(2)
    waves.setsampwidth(l.get_sample_size(pyaudio.paInt16))
    waves.setframerate(fs)
    waves.writeframes(b''.join(li))
    waves.close()

    l.terminate()

    newdata = []
    feats = feature('rec.wav')
    d=np.zeros((64,12))
    for i in range(len(feats)):
        d[i:,]=feats[i]
    x=np.expand_dims(d,axis=0)    
    n = mymodel.predict(x)
    soundclass = int((n > 0.5).astype("int32"))
    print(soundclass)
    print(n)
    print("Detecting....")
    
    os.remove('rec.wav')

    threading.Timer(record_second, doafter5).start()


if __name__ == '__main__':
    # print('Detecting......')
    # newdata = []
    # feats = feature('D:\\HK2-Năm 3\\PBL5\\Code\\Smart_cradle_system\\untitled2.wav') 
    # # print(feats.shape)
    # d=np.zeros((64,12))
    # for i in range(len(feats)):
    #     d[i:,]=feats[i]
    # x=np.expand_dims(d,axis=0)
    # soundclass = int((mymodel.predict(x) > 0.5).astype("int32"))

    # print("Detecting....")
    # print(soundclass)
    # print(mymodel.predict(x))
    doafter5()
