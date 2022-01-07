from rest_framework.views import exception_handler

from rest_framework.exceptions import APIException


def custom_exception_handler(exc, context):     # Custom handler
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    new_response_data = {}
    # checks if the raised exception is of the type you want to handle
    if isinstance(exc, APIException):
        new_response_data['code'] = '400'
        for k, v in response.data.items():
            new_response_data['message'] = {
                'column': k,
                'details': v
            }
        response.data = new_response_data
    return response
