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
import RPi.GPIO as GPIO 
import pyrebase
import time
import firebase_admin
from firebase_admin import credentials, messaging
model_path ='/home/admin/PBL5_BabyCryingDetection_raspberry/Raspberry pi  application/model.tflite'
with open(model_path,'rb') as f:
    model_content = f.read()
# load model to interpreter
interpreter = tflite.Interpreter(model_content = model_content)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


fs = 44100

def feature(soundfile):
    s,r=sf.read(soundfile)
    # s=butter_lowpass_filter(s,11025,44100,order=3)
    x=np.array_split(s,64)
    
    logg=np.zeros((64,12))
    for i in range(len(x)):

        m=np.mean(mfcc(x[i],r, numcep=12,nfft=2048),axis=0)
        logg[i,:]=m

    return logg  

def upload(file_path):
    config = {
        "apiKey": "AIzaSyA14VGe03dQqy5pmrFAxkzpYRHhc4i7Tl0",
        "authDomain": "smart-cradle-application-7cc0d.firebaseapp.com",
        "databaseURL": "https://smart-cradle-application-7cc0d-default-rtdb.firebaseio.com",
        "projectId": "smart-cradle-application-7cc0d",
        "storageBucket": "smart-cradle-application-7cc0d.appspot.com",
        "messagingSenderId": "923331417339",
        "appId": "1:923331417339:web:d1042a05dc64f2e37d0c5e",
        "measurementId": "G-XQQ4RCNPJX",
    }
    firebase = pyrebase.initialize_app(config=config)
    auth = firebase.auth()
    email = 'raspberry@gmail.com'
    password = 'raspberry'
    auth.sign_in_with_email_and_password(email=email, password=password)
    print("login successed")

    storage = firebase.storage()
    cloundfilename = 'audios/test_upload_2.wav'
    filename = file_path
    storage.child(cloundfilename).put(filename)
    print("upload successed")

    cred = credentials.Certificate("Raspberry pi  application\smartCradle_3.json")
    firebase_admin.initialize_app(
        cred, {'storageBucket': "smart-cradle-application-7cc0d.appspot.com"})
    message = messaging.Message(
        notification=messaging.Notification(
            title="Baby crying detected",
            body="Em bé đang khóc nhè",
        ),
        token='cmpV-4jLQBOPcZ3NykSSdg:APA91bGEfrb5SN0obNzTfQTpxWI-4AbNoWt7f5_tCbFKrTnkeTFPRuLVNy6p9ohBsoy5stG9CclSAUQIUuvhizwYGRz5FUg7vT9lQMRR_f-T4nLo1yoRHVYMf1FOUHP0kfpX4VbksJp1',
    )
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    
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
        Ab.swing()
        upload('rec.wav')

    os.remove('rec.wav')
    threading.Timer(3.0, doafter5).start()
    
if __name__ == '__main__':
    
    # Ab = AlphaBot()
    
    # print('Detecting......')
    # newdata = []
    # x = feature('/home/admin/PBL5_BabyCryingDetection_raspberry/Louise_01.m4a_0.wav')
    # x = np.array(x).astype('float32')
    # x = np.expand_dims(x, axis=0)
    # print(x.shape)
    # # Chạy model
    # interpreter.set_tensor(input_details[0]['index'], x)
    # interpreter.invoke()
    # output_data = interpreter.get_tensor(output_details[0]['index'])
    # soundclass = int(output_data > 0.2)
    # print(soundclass)
    # print(output_data)
    # if soundclass !=0 :
    #     upload('/home/admin/PBL5_BabyCryingDetection_raspberry/Louise_01.m4a_0.wav')
    #     Ab.swing()
    upload("Louise_01.m4a_0.wav")
    # doafter5()
