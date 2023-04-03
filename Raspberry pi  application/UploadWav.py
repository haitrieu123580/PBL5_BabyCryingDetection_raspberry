import pyrebase
config = {
    'apiKey': "AIzaSyAM0MseLOCEPKQVKVF-O0ZoHVwu7X14ecg",
    "authDomain": "test-app-a74f1.firebaseapp.com",
    "projectId": "test-app-a74f1",
    "storageBucket": "test-app-a74f1.appspot.com",
    "messagingSenderId": "236232065512",
    "appId": "1:236232065512:web:f824cf5ef653a013c5a45d",
    "measurementId": "G-C7GVFRF735",
    "serviceAccount":'Raspberry pi  application\serviceAccount.json',
    "databaseURL":'https://test-app-a74f1-default-rtdb.firebaseio.com/'
}
firebase = pyrebase.initialize_app(config=config)
storage = firebase.storage()
storage.child('sound_test.wav').put('Louise_01.m4a_0.wav')