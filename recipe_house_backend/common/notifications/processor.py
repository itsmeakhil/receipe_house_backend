from blue_agilis_backend.common.notifications.handlers import email as email_handler


def send_notification(notification):
    """
    send email notification
    Note:
        'from_email' will be taken from 'settings.SENDGRID_EMAIL_FROM'
    Usage:
        payload = {
            'type': "email",
            'to_emails': "username@gmail.com",
            'subject': "sample subject",
            'message': 'sample email message',
        }
                or

        payload = {
            'type': "email",
            'to_emails': "username@gmail.com",
            'subject': "sample subject",
            'message': '', // generated data from template_context comes here
            'template_name': 'successful.html',
            'template_context': {'key': 'value'},
        }
        send_notification(payload)
    """
    if notification['type'] == "email":
        print('in notification')
        return email_handler.send(notification)
