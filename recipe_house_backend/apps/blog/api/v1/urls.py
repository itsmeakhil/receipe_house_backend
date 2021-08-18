"""
Claims API V1
"""
from rest_framework import routers

from recipe_house_backend.apps.blog.api.v1.api_views import TagViewSet, BlogViewSet

blog_router = routers.DefaultRouter()
blog_router.register(r'blog', BlogViewSet)
blog_router.register(r'tag', TagViewSet)
