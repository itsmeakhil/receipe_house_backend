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
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import token_obtain_pair

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
from recipe_house_backend.common.utils.http_helper import logger
from recipe_house_backend.common.utils.response_helper import create_internal_response, Status, create_http_response

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

    def get_permissions(self):
        if self.action in ['create', 'forgot_password', 'reset_password']:
            return (permissions.AllowAny(),)
        return [permissions.IsAuthenticated()]

    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            user = serializer.save()
            logger.info('User added successfully')
            try:
                return self._send_activation_mail(user)
            except Exception as e:
                logger.error(e.__str__())
                return HttpResponse(e.__str__())

    def _send_activation_mail(self, user):
        logger.info('Starting to send verification Mail')
        link = f'{settings.BASE_URL}/api/v1/users/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/' \
               f'{account_activation_token.make_token(user)}/'
        subject = "Activate your Blue Agilis account"
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'link': link,
            'subject': subject

        })
        return send_templated_mail(subject, message, [user.email])

    @action(detail=False,
            methods=['post'],
            serializer_class=EmailSerializer,
            url_path='forgot_password')
    def forgot_password(self, request, pk=None):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                self.__send_forgot_password_email(user)
                msg = 'Password reset email has been sent'
                response = create_internal_response(Status.ok, msg)
            else:
                response = create_internal_response(Status.badrequest, serializer.errors)

            return create_http_response(response)

        except Exception as e:
            logger.exception("Forgot Password API Failed")
            response = create_internal_response(Status.error, "Internal Server Error")
            return create_http_response(response)

    @action(detail=False,
            methods=['post'],
            serializer_class=PasswordSerializer,
            url_path='reset_password')
    def reset_password(self, request, pk=None):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                msg = 'Password has been changed'
                response = create_internal_response(Status.ok, msg)
            else:
                response = create_internal_response(Status.badrequest, serializer.errors)

            return create_http_response(response)

        except Exception as e:
            logger.exception("Reset Password API Failed")
            response = create_internal_response(Status.error, "Internal Server Error")
            return create_http_response(response)

    @action(detail=False,
            methods=['post'],
            serializer_class=PasswordChangeSerializer,
            url_path='change_password')
    def change_password(self, request, pk=None):
        try:
            if self.request.data['new_password'] != self.request.data['confirm_password']:
                msg = 'New passwords are not matching'
                response = create_internal_response(Status.badrequest, msg)
                return create_http_response(response)

            if self.request.data['new_password'] == self.request.data['old_password']:
                msg = 'Old Password and New password cannot be same '
                response = create_internal_response(Status.badrequest, msg)
                return create_http_response(response)

            user = User.objects.get(pk=self.request.user.id)
            if authenticate(email=user.email, password=self.request.data['old_password']):
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    user.set_password(self.request.data['new_password'])
                    user.save()
                    msg = 'Password has been changed'
                    response = create_internal_response(Status.ok, msg)
                else:
                    response = create_internal_response(Status.badrequest, serializer.errors)
                return create_http_response(response)
            msg = 'Unable to login, Please check email or password.'
            response = create_internal_response(Status.badrequest, msg)
            return create_http_response(response)

        except Exception as e:
            logger.exception("Change Password API Failed", e)
            response = create_internal_response(Status.error, "Internal Server Error")
            return create_http_response(response)

    def __send_forgot_password_email(self, user):
        """Send email to user when forgot password"""
        context = {
            'uid': encode_uid(user.pk),
            'token': generate_user_token(user),
        }
        # Link of Stand alone UI page for set new password
        # "http://<host>/api/v1/set_password/{uid}/{token}/"
        url = (settings.PASSWORD_SET_URL).format(**context)
        subject = 'Blue Agilis - Reset Password'
        message = render_to_string('forgot_password.html', {
            'link': url,
            'user_name': user.get_full_name() or 'user'

        })
        return send_templated_mail(subject, message, [user.email])

    @action(detail=False,
            methods=['get'],
            serializer_class=UserDetailsSerializer,
            url_path='details')
    def user_details(self, request):
        try:
            user = User.objects.get(pk=request.user.id)
            serializer = self.get_serializer(user)
            response = create_internal_response(Status.ok, serializer.data)
            return create_http_response(response)
        except Exception as e:
            logger.exception("User Details API Get failed", e)
            response = create_internal_response(Status.error, "Internal Server Error")
            return create_http_response(response)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        login(request, user)
        access_token = get_tokens_for_user(user)
        context = {
            'refresh': access_token['refresh'],
            'access': access_token['access'],
        }
        redirect_url = (settings.USER_ACTIVATION_URL).format(**context)
        return redirect(redirect_url)
    else:
        return HttpResponse('Activation link is invalid!')


@permission_classes((AllowAny,))
class UserLogin(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(email=email, password=password)
        if user is None:
            msg = 'Unable to login, Please check email or password.'
            response = create_internal_response(Status.badrequest, msg)
            return create_http_response(response)
        if not user.is_verified:
            msg = 'Please confirm the email and the try again.'
            response = create_internal_response(Status.badrequest, msg)
            return create_http_response(response)
        response = get_tokens_for_user(user)
        user_serializer = UserDetailsSerializer(user)
        response['user_data'] = user_serializer.data

        return Response(response)
