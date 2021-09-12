import json

import requests

from recipe_house_backend.settings import FCM_TOKEN



class FcmNotificationPusher:
    def __init__(self):
        self.fcm_token = FCM_TOKEN

    def send_notification(self, device_token, title):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + self.fcm_token,
        }

        body = {
            'notification': {'title': title,
                             'body': 'You have a new notification from Change The Wold'
                             },
            'to': device_token,
            'priority': 'high',
        }
        response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        return response

