from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer


class CSRFToken(APIView):   # Request csrf token class
    permission_classes = (AllowAny,)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({
            'code': 'success',
            'message': 'CSRF injected.'
        }, status=status.HTTP_200_OK)


class LoginView(APIView):   # Request login information class
    SERIALIZER_CLASS = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.SERIALIZER_CLASS(data=request.data)
        serializer.is_valid(raise_exception=True)
        acc, ref = serializer.clean_user
        context = {
            'access_token': acc,
            'refresh_token': ref,
        }
        return Response({
            'code': 'success',
            'message': context
        }, status=status.HTTP_200_OK)


class RegisterView(APIView):    # Request register new user class
    SERIALIZER_CLASS = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.SERIALIZER_CLASS(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = serializer.data
        return Response({
            'code': 'success',
            'message': context
        }, status=status.HTTP_201_CREATED)
