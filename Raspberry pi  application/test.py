import os
import numpy as np
import threading
import pyaudio
import wave
import soundfile as sf
import time


import numpy as np

import tflite_runtime.interpreter as tflite
fs = 44100


model_path = '/home/admin/PBL5_BabyCryingDetection_raspberry/Raspberry pi  application/model.tflite'
with open(model_path,'rb') as f:
    model_content = f.read()
interpreter = tflite.Interpreter(model_content=model_content)
interpreter.allocate_tensors()
