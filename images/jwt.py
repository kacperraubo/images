"""
Filename: tests.py
Author: Kacper Raubo
Creation date: 03/08/2023

Provides JWT token-based authentication for Django REST Framework views.
This authentication backend expects the token to be included in the
request headers as the value of the 'Authorization' field in the format
'Bearer <token>'.
"""

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):
    """
    JWT authentication backend.

    The JWT token should be passed in the 'Authorization' header as 'Bearer <token>'.
    If the token is valid, the user object will be added to the request object and
    can be accessed in the view using 'request.user'.

    If the token is invalid, an 'AuthenticationFailed' exception will be raised and
    the request will be rejected with a 401 Unauthorized status code.

    Note: This implementation assumes that the token is signed with the HS256
    algorithm and uses the Django user model for authentication.

    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            auth_token = auth_header.split(' ')[1]
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])

            user = User.objects.get(username=payload['username'])

            return (user, None)

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
            raise AuthenticationFailed('Invalid token')
