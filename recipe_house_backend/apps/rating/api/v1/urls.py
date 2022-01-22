"""
Claims API V1
"""
from rest_framework import routers


from recipe_house_backend.apps.rating.api.v1.api_views import RatingViewSet,CommentViewSet

rating_router = routers.DefaultRouter()
rating_router.register(r'rating', RatingViewSet)
rating_router.register(r'comment', CommentViewSet)
