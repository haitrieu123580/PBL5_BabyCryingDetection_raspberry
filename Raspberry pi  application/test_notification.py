import firebase_admin
from firebase_admin import credentials, messaging

def noti():
    cred = credentials.Certificate("Raspberry pi  application\smartCradle_3.json")
    firebase_admin.initialize_app(cred,{'storageBucket': "smart-cradle-application-7cc0d.appspot.com"})
    message = messaging.Message(
        notification=messaging.Notification(
            title="Baby crying detected",
            body="Em bé đang khóc nhè",
        ),
        token='cmpV-4jLQBOPcZ3NykSSdg:APA91bGEfrb5SN0obNzTfQTpxWI-4AbNoWt7f5_tCbFKrTnkeTFPRuLVNy6p9ohBsoy5stG9CclSAUQIUuvhizwYGRz5FUg7vT9lQMRR_f-T4nLo1yoRHVYMf1FOUHP0kfpX4VbksJp1',
    )
    # Send a message to devices subscribed to the combination of topics
    # specified by the provided condition.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)

