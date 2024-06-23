from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .serializers import CustomAuthTokenSerializer

User = get_user_model()


class TokenObtainView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    
    @swagger_auto_schema(
        request_body= CustomAuthTokenSerializer,
        responses= {
            200:CustomAuthTokenSerializer,
            400: 'Invalid request data'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        custom_response = {
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name if hasattr(user, 'middle_name') else None,
        }

        return Response(custom_response)


class LogoutView(APIView):
    def post(self, request):
        # Check for authentication
        if not request.user.is_authenticated:
            raise AuthenticationFailed('You are not authenticated')

        # Get the token object for the user
        token, _ = Token.objects.get_or_create(user=request.user)

        # Delete the token
        token.delete()

        return Response({"message": "Successfully logged out."})