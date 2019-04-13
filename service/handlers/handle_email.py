import datetime

from django_celery_results.models import TaskResult

from base.celery import CeleryTask
from service.constants import MAIL_REPORT, TASK_SEND_EMAIL


class SendEmail:
    def process_email_to_user(self, data, filepath, user_list):
        if not user_list and not data.get('email').strip():
            return {
                'message': 'Please give receivers email Id'
            }
        CeleryTask.send(TASK_SEND_EMAIL, kwargs={
            'message': data.get('body').strip(),
            'subject': data.get('subject'),
            'receivers': user_list if user_list else [data.get('email')],
            'cc': [data.get('cc')],
            'bcc': [data.get('bcc')],
            'attachments': [filepath] if filepath else []
        })
        return {
            'message': 'Email sent successfully'
        }

    def every_hour_emails(self):
        created_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        task_objs = TaskResult.objects.filter(date_done__gte=created_time)
        if len(task_objs) >= 1:
            file_path = self.create_mail_report(task_objs)
            CeleryTask.send(
                TASK_SEND_EMAIL,
                kwargs={
                    'subject': 'Email Statistics for {}'.format(
                                str(datetime.datetime.now())),
                    'message': 'Please find attached email report',
                    'receivers': ['prashantwinner1@gmail.com'],
                    'attachments': [file_path],
                })

    def create_mail_report(self, objs):
        file = MAIL_REPORT.format(str(datetime.datetime.now()))
        f = open(file, 'w')
        headers = (
            'task_id,status,time'
            '\n')
        f.write(headers)
        for obj in objs:
            task_id = obj.task_id
            status = obj.status
            time = str(obj.date_done)
            f.write(task_id + ',' + status + ',' + time + '\n')
        return file


def add_tenant_mail_to_user(self):
    subject = 'Added As a Tenant for Flat'
    receivers = 'sharma.pacific1@gmail.com'
    CeleryTask.send(TASK_SEND_EMAIL, kwargs={
        'message': 'without call  ',
        'subject': subject,
        'receivers': [receivers],

    })
