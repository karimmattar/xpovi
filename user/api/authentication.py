import jwt

from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
from django.contrib.auth import get_user_model


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class SafeJWTAuthentication(BaseAuthentication):    # User Authentication

    def authenticate(self, request):

        User = get_user_model()
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed({'code': '401', 'message': 'token expired'})
        except IndexError:
            raise exceptions.AuthenticationFailed({'code': '401', 'message': 'token prefix missing'})
        except Exception as e:
            raise exceptions.AuthenticationFailed({'code': '403', 'message': 'invalid token %s' % e})

        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed({'code': '404', 'message': 'user not found'})

        if not user.is_active:
            raise exceptions.AuthenticationFailed({'code': '403', 'message': 'user is inactive'})

        self.enforce_csrf(request)
        return user, None

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck(request)
        # Populates request.META['CSRF_COOKIE'], which is used in process_view()
        # Set headers['X_CSRFToken']
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
