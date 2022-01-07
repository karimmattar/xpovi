import datetime
import jwt

from django.conf import settings
from django.utils import timezone


def generate_access_token(user):    # Short time token
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=30),
        'iat': datetime.datetime.now(tz=timezone.utc),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):   # Long time token
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=365),
        'iat': datetime.datetime.now(tz=timezone.utc),
        'token': user.auth_token.key
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

    return refresh_token
