from rest_framework import filters
from rest_framework import viewsets

from recipe_house_backend.apps.post.api.v1.serializers import (
    TagSerializer,
    CuisineSerializer,
    CategorySerializer,
    PostSerializer, PostListSerializer
)
from recipe_house_backend.apps.post.models import Tag, Post, Category, Cuisine
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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Category
    """
    queryset = Category.objects.get_all_active()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CuisineViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Cuisine
    """
    queryset = Cuisine.objects.get_all_active()
    serializer_class = CuisineSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Post
    """
    queryset = Post.objects.get_by_filter()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PostListSerializer
        return self.serializer_class
