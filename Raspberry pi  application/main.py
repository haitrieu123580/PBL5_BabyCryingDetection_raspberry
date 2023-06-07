import os
import numpy as np
import threading
import pyaudio
import wave
import soundfile as sf
import time
import tflite_runtime.interpreter as tflite
from scipy.signal import butter, lfilter
from python_speech_features import mfcc
from turn import AlphaBot
import pyrebase
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
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

model_path = '/home/admin/PBL5_BabyCryingDetection_raspberry/Models/model11.tflite'
with open(model_path, 'rb') as f:
    model_content = f.read()

# Load model to interpreter
interpreter = tflite.Interpreter(model_content=model_content)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

fs = 44100

def feature(soundfile):
    s, r = sf.read(soundfile)
    x = np.array_split(s, 64)

    logg = np.zeros((64, 12))
    for i in range(len(x)):
        m = np.mean(mfcc(x[i], r, numcep=12, nfft=2048), axis=0)
        logg[i, :] = m

    return logg  

# Upload img and audio
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

# Send notification
cred = credentials.Certificate("/home/admin/PBL5_BabyCryingDetection_raspberry/Raspberry pi  application/smartCradle_3.json")
firebase_admin.initialize_app(
    cred, {'storageBucket': "smart-cradle-application-7cc0d.appspot.com"})

def upload(file_path_audio, file_path_image):
    storage = firebase.storage()
    clound_audio_filename = 'audios/test_upload_rasp.wav'
    filename_audio = file_path_audio
    storage.child(clound_audio_filename).put(filename_audio)
    clound_image_filename = 'images/test_upload_rasp.jpg'
    filename_image = file_path_image
    storage.child(clound_image_filename).put(filename_image)
    print("Upload successed")

    message = messaging.Message(
        notification=messaging.Notification(
            title="Baby crying detected",
            body="Baby is crying!!!",
        ),
        token='cmpV-4jLQBOPcZ3NykSSdg:APA91bGEfrb5SN0obNzTfQTpxWI-4AbNoWt7f5_tCbFKrTnkeTFPRuLVNy6p9ohBsoy5stG9CclSAUQIUuvhizwYGRz5FUg7vT9lQMRR_f-T4nLo1yoRHVYMf1FOUHP0kfpX4VbksJp1',
    )
    response = messaging.send(message)

def swing():
    Ab = AlphaBot()
    Ab.swing()
def capture_and_upload():
	camera.capture()
	upload('rec.wav', 'baby_image.jpg')
def save_audio():
	return 0
def detect_and_process():
    while True:
        try:
            # Start record
            start_record = time.time()
            l = pyaudio.PyAudio()
            livesound = l.open(format=pyaudio.paInt16,
                               channels=1,
                               rate=fs,
                               input=True,
                               frames_per_buffer=8192,
                               input_device_index=2)
            livesound.start_stream()
           
            print("Recording...")

            # Record audio for 2 seconds
            frames = []
            for i in range(0, int(fs / 8192 * 2)):
                data = livesound.read(8192)
                frames.append(data)

            # Stop recording
            livesound.stop_stream()
            livesound.close()
            l.terminate()

            print(f'end record {time.time()-start_record} ')
			
            # Save audio to file
            start_save_audio = time.time()
            audio_file = "rec.wav"
            waves = wave.open('rec.wav', 'w')
            waves.setnchannels(1)
            waves.setsampwidth(l.get_sample_size(pyaudio.paInt16))
            waves.setframerate(fs)
            waves.writeframes(b''.join(frames))
            waves.close()
            print(f'end save audio {time.time()-start_save_audio} ')
            # Process audio
            audio_features = feature(audio_file)
            audio_features = np.array(audio_features).astype('float32')
            audio_features = np.expand_dims(audio_features, axis=0)
            
            # Run inference
            start_detect = time.time()
            interpreter.set_tensor(input_details[0]['index'], audio_features)
            interpreter.invoke()
            output = interpreter.get_tensor(output_details[0]['index'])
            soundclass = int(output>=0.6)
            print(f'end detect {time.time()-start_detect} ')
            print(soundclass)
            print(output)
            if soundclass ==1:
                print("Baby crying detected!")
                # Take picture
                #camera.capture()
                # Create threads for capture_upload and swing
                upload_thread = threading.Thread(target=capture_and_upload)
                swing_thread = threading.Thread(target=swing)
                # Start threads
                start_upload = time.time()
                upload_thread.start()
                start_swing = time.time()
                swing_thread.start()
                # Wait for threads to finish
                upload_thread.join()
                print(f'end upload {time.time()-start_upload} ')
                swing_thread.join()
                print(f'end swing {time.time()-start_swing} ')
            else:
                print("No baby crying detected.")

            # Delete audio and image files
            os.remove("rec.wav")
            # os.remove("baby_image.jpg")

            # Calculate elapsed time
            end_record = time.time()
            elapsed_time = end_record - start_record
            print("Elapsed time: %.2f seconds" % elapsed_time)

            # Wait for 1 second before detecting again
            time.sleep(1)

        except KeyboardInterrupt:
            break

detect_and_process()
