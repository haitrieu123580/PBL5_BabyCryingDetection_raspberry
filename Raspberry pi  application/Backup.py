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
import camera

# Tắt các thông báo lỗi từ ALSA
from ctypes import *
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
	print('skipping error message')
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
#set error handler
asound.snd_lib_error_set_handler(c_error_handler)



model_path ='/home/admin/PBL5_BabyCryingDetection_raspberry/Models/model10.tflite'
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

# upload img and audio
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

# send noti
cred = credentials.Certificate("/home/admin/PBL5_BabyCryingDetection_raspberry/Raspberry pi  application/smartCradle_3.json")
firebase_admin.initialize_app(
    cred, {'storageBucket': "smart-cradle-application-7cc0d.appspot.com"})


def upload(file_path_audio, file_path_image):

    # auth = firebase.auth()
    # email = 'raspberry@gmail.com'
    # password = 'raspberry'
    # auth.sign_in_with_email_and_password(email=email, password=password)
    # print("login successed")

    storage = firebase.storage()
    clound_audio_filename = 'audios/test_upload_rasp.wav'
    filename_audio = file_path_audio
    storage.child(clound_audio_filename).put(filename_audio)
    clound_image_filename = 'images/test_upload_rasp.jpg'
    filename_image = file_path_image
    storage.child(clound_image_filename).put(filename_image)
    print("upload successed")


    message = messaging.Message(
        notification=messaging.Notification(
            title="Baby crying detected",
            body="baby is crying!!!",
        ),
        token='cmpV-4jLQBOPcZ3NykSSdg:APA91bGEfrb5SN0obNzTfQTpxWI-4AbNoWt7f5_tCbFKrTnkeTFPRuLVNy6p9ohBsoy5stG9CclSAUQIUuvhizwYGRz5FUg7vT9lQMRR_f-T4nLo1yoRHVYMf1FOUHP0kfpX4VbksJp1',
    )
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:')
    
def doafter5():
    while True:
        try:
			#start record
            start_record = time.time()
            l = pyaudio.PyAudio()
            livesound = l.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=fs,
                                input=True,
                                frames_per_buffer=8192,input_device_index = 2)
            livesound.start_stream()
            li = []
            Livesound = None
            for f in range(0, int(fs/8192*5)):
                Livesound = livesound.read(8192)
                li.append(Livesound)
            livesound.stop_stream()
            livesound.close()
            
            waves = wave.open('rec.wav', 'w')
            waves.setnchannels(1)
            waves.setsampwidth(l.get_sample_size(pyaudio.paInt16))
            waves.setframerate(fs)
            waves.writeframes(b''.join(li))
            waves.close()
            l.terminate()
            print(f'stop record {time.time()-start_record}')
            
            x = feature('rec.wav')
            x = np.array(x).astype('float32')
            x = np.expand_dims(x, axis=0)
            # Chạy model
            start_detect = time.time()
            interpreter.set_tensor(input_details[0]['index'], x)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            soundclass = int(output_data >= 0.6)
            print(f'stop detect {time.time()-start_detect}')
            print("Detecting....")
            print(soundclass)
            print(output_data)
            
            Ab = AlphaBot()
            if soundclass == 1:
                start_cap = time.time()
                #camera.capture()
                print(f'stop cap {time.time()-start_cap}')
                start_upload = time.time()
                upload('rec.wav', 'baby_image.jpg')
                print(f'stop upload {time.time()-start_upload}')
                start_swing = time.time()
                Ab.swing()
                print(f'stop swing {time.time()-start_swing}')
            else:
                print('not baby crying sound')
        except OSError as e:
            if e.errno == -9996 or e.errno == -9981 or e.errno == -9984:
                # Ignore 'Alsa lib...' error
                continue
            else:
                print(f'ALSA error: {e}')
        except Exception as e:
            print(f"Erorr: {e}")
			
        # Tạm dừng chương trình trong vòng 20 giây
        time.sleep(20)

    
if __name__ == '__main__':
    
    doafter5()
