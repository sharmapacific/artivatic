from celery import shared_task
from celery.decorators import periodic_task
from celery.schedules import crontab
from django.conf import settings
from django.core.mail.message import EmailMessage

from base.exceptions import EmailReceiverNotProvided
from service.constants import FORMAT_HTML, TASK_SEND_EMAIL
from service.handlers.handle_email import SendEmail


def get_receivers(receivers):
    if isinstance(receivers, (list, tuple)):
        receivers = [email for email in receivers if email]
    if not receivers:
        raise EmailReceiverNotProvided()
    if isinstance(receivers, str):
        return list(filter(None, [x.strip() for x in receivers.split(',')]))
    return receivers


@shared_task(name=TASK_SEND_EMAIL)
def send_email(subject, message, receivers, **kwargs):
    receivers = get_receivers(receivers)
    sender = kwargs.get('sender', settings.EMAIL_HOST_USER)
    category = kwargs.get('category')
    attachments = kwargs.get('attachments', [])

    email_kwargs = {}
    for arg in ['bcc', 'cc', 'reply_to', 'headers']:
        email_kwargs[arg] = kwargs.get(arg)

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=sender,
        to=receivers,
        **email_kwargs
    )
    email.content_subtype = FORMAT_HTML

    # As 'NoneType' object is not iterable.
    if attachments:
        for file_path in attachments:
            email.attach_file(file_path)

    email_result = email.send()

    email_kwargs.update({
        'category': category,
        'result': email_result,
        'receivers': receivers,
        'attachments': attachments,
        'sender': sender,
        'subject': subject,
        'message': message
    })

    return email_kwargs


@periodic_task(run_every=crontab(minute='*/30'), name='check_new_emails')
def check_new_emails():
    SendEmail().every_hour_emails()
