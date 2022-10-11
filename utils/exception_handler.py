from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
          
    return response