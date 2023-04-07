import pyrebase
import datetime

config = {
    "apiKey": "AIzaSyA14VGe03dQqy5pmrFAxkzpYRHhc4i7Tl0",
    "authDomain": "smart-cradle-application-7cc0d.firebaseapp.com",
    "databaseURL": "https://smart-cradle-application-7cc0d-default-rtdb.firebaseio.com",
    "projectId": "smart-cradle-application-7cc0d",
    "storageBucket": "smart-cradle-application-7cc0d.appspot.com",
    "messagingSenderId": "923331417339",
    "appId": "1:923331417339:web:d1042a05dc64f2e37d0c5e",
    "measurementId": "G-XQQ4RCNPJX",
    "serviceAccount":'PBL5_BabyCryingDetection_training\Baby Cry Detection\Raspberry pi  application\smartCradle_3.json',
}
firebase = pyrebase.initialize_app(config=config)
# authenticate with firebase
auth = firebase.auth()
email = "tayvuong@gmail.com"
password = "Vuongviettay123"
user = auth.sign_in_with_email_and_password(email, password)
access_token = 'UesIQ4SLkuUwPVplMZDlbpcfzQL2'
print(access_token)

storage = firebase.storage()
folder_name ='audios'
filename = 'sound_test_PC_5.wav'
filepath ='PBL5_BabyCryingDetection_training\Louise_01.m4a_0.wav'
storage.child(folder_name + "/" + filename).put(filepath)
file_url = storage.child(filename).get_url(token=access_token)

db = firebase.database()
folder_name = 'audios'
audio_ref = db.child(folder_name).push(file_url)

