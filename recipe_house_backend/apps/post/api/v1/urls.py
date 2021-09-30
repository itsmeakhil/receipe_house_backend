"""
Claims API V1
"""
from rest_framework import routers

from recipe_house_backend.apps.post.api.v1.api_views import(
    TagViewSet,
    PostViewSet,
    CuisineViewSet,
    CategoryViewSet
)

post_router = routers.DefaultRouter()
post_router.register(r'post', PostViewSet)
post_router.register(r'tag', TagViewSet)
post_router.register(r'cuisine', CuisineViewSet)
post_router.register(r'category', CategoryViewSet)
