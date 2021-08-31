from rest_framework import filters
from rest_framework import viewsets

from recipe_house_backend.apps.blog.api.v1.serializers import (
    TagSerializer,
    BlogSerializer
)
from recipe_house_backend.apps.blog.models import Tag, Blog
from recipe_house_backend.common.utils.helper import soft_delete_model_instance


class TagViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Tag
    """
    queryset = Tag.objects.get_all_active()
    serializer_class = TagSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)

    search_fields = ('name',)

    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class BlogViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Blog
    """
    queryset = Blog.objects.get_by_filter()
    serializer_class = BlogSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title')

    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
