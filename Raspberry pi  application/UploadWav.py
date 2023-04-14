import pyrebase
import firebase_admin
from firebase_admin import credentials, messaging
config = {
    "apiKey": "AIzaSyA14VGe03dQqy5pmrFAxkzpYRHhc4i7Tl0",
    "authDomain": "smart-cradle-application-7cc0d.firebaseapp.com",
    "databaseURL": "https://smart-cradle-application-7cc0d-default-rtdb.firebaseio.com",
    "projectId": "smart-cradle-application-7cc0d",
    "storageBucket": "smart-cradle-application-7cc0d.appspot.com",
    "messagingSenderId": "923331417339",
    "appId": "1:923331417339:web:d1042a05dc64f2e37d0c5e",
    "measurementId": "G-XQQ4RCNPJX",
    # "serviceAccount": 'PBL5_BabyCryingDetection_training\Baby Cry Detection\Raspberry pi  application\smartCradle_3.json',
}
firebase = pyrebase.initialize_app(config=config)
auth = firebase.auth()
email = 'raspberry@gmail.com'
password = 'raspberry'
auth.sign_in_with_email_and_password(email=email, password=password)
print("login successed")

storage = firebase.storage()
cloundfilename = 'audios/test_upload_2.wav'
filename = 'Louise_01.m4a_0.wav'
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
