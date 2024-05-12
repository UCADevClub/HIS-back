from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class UserTokenObtainView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(UserTokenObtainView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response['token'])
        return Response(
            {
                'token': token.key,
                'user_id': token.user_id,
            },
            status=status.HTTP_200_OK
        )
