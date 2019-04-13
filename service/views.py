import csv
import os

from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.views import APIView

from service.handlers.handle_email import SendEmail


class SendEmailView(APIView):
    def get(self, request):
        return render(request, 'email_ui.html')

    def post(self, request):
        data = request.data
        file_path = None
        user_list = None
        file1 = request.FILES.get('attachment')
        file2 = request.FILES.get('csv_mail')
        if file1:
            file_path = self.get_file_path(file1)
        if file2:
            user_list = self.get_email_list(file2)
        response = SendEmail().process_email_to_user(
            data, file_path, user_list)
        if isinstance(response, dict):
            messages.info(request, response['message'])
        return render(request, 'email_ui.html')

    def get_file_path(self, attachment):
        fs = FileSystemStorage()
        filename = fs.save(attachment.name, attachment)
        file_url = fs.url(filename)
        return os.path.join(settings.BASE_DIR + file_url)

    def get_email_list(self, file2):
        file_path = self.get_file_path(file2)
        with open(file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            mail_list = []
            for row in csv_reader:
                mail_list.append(row['email_id'])
        return mail_list
