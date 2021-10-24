"""
Claims API V1
"""
from rest_framework import routers

from recipe_house_backend.apps.favourites.api.v1.api_views import FavouritePostViewSet

favourite_post_router = routers.DefaultRouter()

favourite_post_router.register(r'favourite-post', FavouritePostViewSet)
