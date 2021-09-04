from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



def make_content(notification):
    if not notification.get('template_name', None):
        return notification['message']

    return render_to_string(notification['template_name'],
                            notification.get('template_context', None))


def send_templated_mail(subject, message, recipient):
    """
    send email to a single recipient
    :param subject: mail subject
    :param message: mail message
    :param recipient: recipient mail address
    :return: status
    """
    email_from = settings.EMAIL_FROM_ADDRESS
    try:
        print(f'In mailer function trying to send mail')
        email = EmailMessage(subject, message, email_from, recipient)
        email.content_subtype = 'html'
        email.send()
        return 'success'
    except Exception as e:
        print(e)
