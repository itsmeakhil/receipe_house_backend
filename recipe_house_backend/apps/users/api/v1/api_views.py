from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from recipe_house_backend.apps.users.api.v1.serializers import (
    UserSerializer,
    UserDetailsSerializer,
    PasswordChangeSerializer,

)
from recipe_house_backend.apps.users.api.v1.service import UserLoginService
from recipe_house_backend.apps.users.models import (
    User
)
from recipe_house_backend.common.utils import response_helper, logger
from recipe_house_backend.common.utils.helper import (
    soft_delete_model_instance
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for User
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email', 'first_name', 'last_name', 'username')

    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)

    @action(detail=False,
            methods=['post'],
            serializer_class=PasswordChangeSerializer,
            url_path='change-password')
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
                    response = response_helper.http_400('Invalid Data', serializer.errors)
                return response
            return response_helper.http_200_message('Unable to login, Please check email or password.')

        except Exception as e:
            logger.error("Unable to change password", e)
            return response_helper.http_500('Unable to change password due to Internal Server Error', e)


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
            return response_helper.http_500('Unable to login to admin panel due to Internal Server Error', e)


@permission_classes((AllowAny,))
class FirebaseLogin(APIView):

    def post(self, request):
        try:
            return UserLoginService.verify_firebase_user(self)
        except Exception as e:
            return response_helper.http_500('Internal server error occurred while login with firebase', e)
