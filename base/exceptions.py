from rest_framework import status
from rest_framework.exceptions import APIException


class EmailReceiverNotProvided(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error Sending Email: '
    default_detail += 'Please provide the email address of the receiver.'
    default_code = 'email_receiver_not_provided'
