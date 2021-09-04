import rest_framework_simplejwt
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from dotenv import load_dotenv
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import token_obtain_pair
from recipe_house_backend.apps.users.api.v1.service import UserLoginService

from recipe_house_backend.apps.users.api.v1.serializers import (
    UserSerializer,
    UserDetailsSerializer,
    EmailSerializer,
    PasswordSerializer,
    PasswordChangeSerializer,

)
from recipe_house_backend.apps.users.models import (
    User
)
from recipe_house_backend.common.notifications.handlers.email import send_templated_mail
from recipe_house_backend.common.services.token_service import account_activation_token
from recipe_house_backend.common.utils.auth_helper import get_tokens_for_user
from recipe_house_backend.common.utils.helper import (
    soft_delete_model_instance,
    generate_user_token,
    encode_uid
)
from recipe_house_backend.common.utils import response_helper, logger

# Load the .env file  and interpolate the values to environment  variables
load_dotenv()

login_200_response_json = {
    "application/json": {
        "refresh": "x.y.z",
        "access": "x.y.z"
    }
}

login_400_response_json = {
    "application/json": {
        "email": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ]
    }
}

login_401_response_json = {
    "application/json": {
        "detail": "No active account found with the given credentials"
    }
}

login_200_response = openapi.Response(description='Login Successful',
                                      examples=login_200_response_json)
login_400_response = openapi.Response(description='Login Failed',
                                      examples=login_400_response_json)
login_401_response = openapi.Response(description='Login Failed',
                                      examples=login_401_response_json)
TokenObtainView = swagger_auto_schema(
    method='post',
    responses={
        200: login_200_response,
        400: login_400_response,
        401: login_401_response,
    },
)(rest_framework_simplejwt.views.token_obtain_pair)

TokenRefreshView = rest_framework_simplejwt.views.token_refresh


class UserViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for User
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name')



    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)


    @action(detail=False,
            methods=['post'],
            serializer_class=PasswordChangeSerializer,
            url_path='change_password')
    def change_password(self, request, pk=None):
        try:
            if self.request.data['new_password'] != self.request.data['confirm_password']:
                return response_helper.http_400_message('New passwords are not matching')
            if self.request.data['new_password'] == self.request.data['old_password']:
                return response_helper.http_400_message('Old Password and New password cannot be same ')

            user = User.objects.get(pk=self.request.user.id)
            if authenticate(email=user.email, password=self.request.data['old_password']):
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    user.set_password(self.request.data['new_password'])
                    user.save()
                    response = response_helper.http_200_message('Password has been changed')
                else:
                    response = response_helper.http_400('Invalid serializer', serializer.errors)
                return response
            return response_helper.http_200_message('Unable to login, Please check email or password.')

        except Exception as e:
            logger.error("Unable to change password", e)
            return response_helper.http_500('Unable to change password due to Internal Server Error' ,e)


@permission_classes((AllowAny,))
class UserLogin(APIView):

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            user = authenticate(email=email, password=password)
            if user is None:
                return response_helper.http_400_message('Unable to login, Please check email or password.')
            if not user.is_verified:
                return response_helper.http_400_message('Please verify the user and the try again.')
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserDetailsSerializer(user)
            response = {
                "token": token.key,
                "user_data": user_data.data
            }
            return response_helper.http_200('User login successfull', response)
        except Exception as e:
            logger.exception("Unable to login to admin panel", e)
            return response_helper.http_500('Unable to login to admin panel due to Internal Server Error' ,e)

@permission_classes((AllowAny,))
class FirebaseLogin(APIView):

    def post(self, request):
        try:
            return UserLoginService.verify_firebase_user(self)
        except Exception as e:
            logger.exception(f"Internal server error occurred : {e}", e)
            return response_helper.http_500('Internal server error occurred while login with firebase', e )
