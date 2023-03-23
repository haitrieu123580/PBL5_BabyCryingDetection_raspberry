import os
import numpy as np
import threading
import pyaudio
import wave
import soundfile as sf
import time
 
import tflite_runtime.interpreter as tflite
from scipy.signal import butter,lfilter
from python_speech_features import mfcc
from turn import AlphaBot

model_path ='/home/admin/PBL5_BabyCryingDetection_raspberry/Raspberry pi  application/model.tflite'
with open(model_path,'rb') as f:
    model_content = f.read()
# load model to interpreter
interpreter = tflite.Interpreter(model_content = model_content)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


fs = 44100
def butter_lowpass(cutoff,fs,order=5):
    nyq=0.5*fs
    normal_cutoff=cutoff/nyq
    b,a=butter(order,normal_cutoff,btype='low',analog=False)
    return b,a
def butter_lowpass_filter(data,cutoff,fs,order=5):
    b,a=butter_lowpass(cutoff,fs,order=order)
    y=lfilter(b,a,data)
    return y

def feature(soundfile):
    s,r=sf.read(soundfile)
    s=butter_lowpass_filter(s,11025,44100,order=3)
    x=np.array_split(s,64)
    
    logg=[]
    for i in x:     
        xx=np.mean(mfcc(i,r,numcep=12,nfft=2048),axis=0)
        logg.append(xx)
        
    return  logg  

def doafter5():
    l = None
    livesound = None
    l = pyaudio.PyAudio()
    livesound = l.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=fs, input=True,frames_per_buffer=8192
                 )
    livesound.start_stream() 
    Livesound = None
    li = []
    
    timeout = time.time()+20
    for f in range(0, int(fs/8192*2)):
        Livesound = livesound.read(8192)
        li.append(Livesound)
        
   
    waves = wave.open('rec.wav','w')
    waves.setnchannels(1)
    waves.setsampwidth(l.get_sample_size(pyaudio.paInt16))
    waves.setframerate(fs)
    waves.writeframes(b''.join(li))
    waves.close()

    l.terminate()

    x = feature('rec.wav')
    x = np.array(x).astype('float32')
    x = np.expand_dims(x, axis=0)
    # Chạy model
    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    soundclass = int(output_data > 0.2)

    print("Detecting....")
    print(soundclass)
    print(output_data)
    
    Ab = AlphaBot()
    if soundclass==1:  
        Ab.forward()
    else:
        Ab.stop()
    os.remove('rec.wav')
    threading.Timer(3.0, doafter5).start()
    
if __name__ == '__main__':
    
    Ab = AlphaBot()
    
    print('Detecting......')
    newdata = []
    x = feature('/home/admin/PBL5_BabyCryingDetection_raspberry/Louise_01.m4a_0.wav')
    x = np.array(x).astype('float32')
    x = np.expand_dims(x, axis=0)
    print(x.shape)
    # Chạy model
    interpreter.set_tensor(input_details[0]['index'], x)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    soundclass = int(output_data > 0.2)
    print(soundclass)
    print(output_data)
    if soundclass !=0 :
        Ab.forward()
    else:
        Ab.stop()
    # doafter5()
