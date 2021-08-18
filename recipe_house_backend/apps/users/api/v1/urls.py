"""
Claims API V1
"""
from rest_framework import routers

from recipe_house_backend.apps.users.api.v1.api_views import (
    UserViewSet
)

user_router = routers.DefaultRouter()
user_router.register(r'users', UserViewSet)
