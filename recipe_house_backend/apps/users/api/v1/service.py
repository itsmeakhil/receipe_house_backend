import firebase_admin
from django.contrib.auth import logout
from django.db import transaction
from firebase_admin import credentials, auth
from rest_framework.authtoken.models import Token

from recipe_house_backend.apps.users.api.v1.serializers import UserSerializer
from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils import response_helper

from recipe_house_backend.common.utils import logger

cred = credentials.Certificate("recipe_house_backend/common/utils/firebase-key.json")
firebase_admin.initialize_app(cred)


class UserLoginService:

    def verify_firebase_user(self):
        try:
            uid = self.request.data['uid']
            device_id = self.request.data['device_id']
            firebase_user = firebase_admin.auth.get_user(uid)
            if firebase_user:
                user_exists = User.objects.filter(uid=uid).exists()
                if user_exists:
                    user = User.objects.get(uid=uid)
                    if device_id:
                        user.device_id = device_id
                        user.save()
                    user_data = UserSerializer(user)
                    token, _ = Token.objects.get_or_create(user=user)
                    data = {
                        "token": token.key,
                        "user_data": user_data.data
                    }
                    return response_helper.http_200('User Login successfull', data)
                serializer = UserSerializer(data=self.request.data)
                if serializer.is_valid():
                    user = serializer.save()
                    user_serializer = UserSerializer(user)
                    user.save()
                    token, _ = Token.objects.get_or_create(user=user)
                    user_data = {
                        "token": token.key,
                        "user_data": user_serializer.data
                    }
                    return response_helper.http_201('User added successfully', user_data)
                return response_helper.http_400('User data validation error', serializer.errors)
            return response_helper.http_404('Firebase user not found')
        except Exception as e:
            return response_helper.http_500(f"Internal server error occurred : {e}")

    def logout(request):
        """Function to logout the current user"""
        with transaction.atomic():
            logout(request)
            msg = 'User logged out successfully'
            return response_helper.http_200_message(msg)

