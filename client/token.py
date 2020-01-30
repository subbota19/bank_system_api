from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = {'token': 'User with this data does not exist'}
        user = User.objects.all().filter(username=request.data['username'])
        if user:
            token, created = Token.objects.get_or_create(user=user[0])
            response = {
                'token': token.key,
                'username': request.data['username'],
            }
        return Response(response)

    def get(self, request, *args, **kwargs):
        return Response({'detail': "send you password and username for generate token"})
