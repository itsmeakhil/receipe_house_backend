from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView

from recipe_house_backend.apps.post.api.v1.serializers import (
    TagSerializer,
    CuisineSerializer,
    CategorySerializer,
    PostSerializer, PostListSerializer, TagUpdateSerializer, CategoryUpdateSerializer, CuisineUpdateSerializer,
    CuisineListSerializer, CategoryListSerializer, TagListSerializer
)
from recipe_house_backend.apps.post.models import Tag, Post, Category, Cuisine
from recipe_house_backend.common.utils import response_helper
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

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return TagUpdateSerializer
        return self.serializer_class


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

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CategoryUpdateSerializer
        return self.serializer_class


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

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CuisineUpdateSerializer
        return self.serializer_class


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


class PostAddMasterData(APIView):
    def get(self, request):
        tags = Tag.objects.get_all_active()
        category = Category.objects.get_all_active()
        cuisine = Cuisine.objects.get_all_active()
        data = {
            'tags': TagListSerializer(tags, many=True).data,
            'category': CategoryListSerializer(category, many=True).data,
            'cuisine': CuisineListSerializer(cuisine, many=True).data
        }
        return response_helper.http_200('Master data loaded', data)
