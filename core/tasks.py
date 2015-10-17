from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from auto_devops.celery import app
import logging
logger = logging.getLogger(__name__)


class SendEmailTask(app.Task):
    """ Send transactional email
    """
    def run(self, subject='', message='', message_html=None, sender=None, recipient=''):
        if not sender:
            sender = settings.EMAIL_NOTIFICATION
        if not subject or not message or not recipient:
            raise Exception('Error sending email, not all required fields were passed')
        message = EmailMultiAlternatives(subject, message, sender, [recipient])
        if message_html:
            message.attach_alternative(message_html, "text/html")
        message.send()
        logging.info('Sent email to %s with subject: %s' % (recipient, subject))
