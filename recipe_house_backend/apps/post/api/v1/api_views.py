from rest_framework import filters
from rest_framework import viewsets
from rest_framework.views import APIView

from recipe_house_backend.apps.post.api.v1.serializers import (
    TagSerializer,
    CuisineSerializer,
    CategorySerializer,
    PostSerializer, PostListAdminSerializer, TagUpdateSerializer, CategoryUpdateSerializer, CuisineUpdateSerializer,
    CuisineListSerializer, CategoryListSerializer, TagListSerializer, PostDetailsSerializer, PostTypeSerializer,
    PostTypeUpdateSerializer
)
from recipe_house_backend.apps.post.models import Tag, Post, Category, Cuisine, PostType
from recipe_house_backend.common.utils import response_helper
from recipe_house_backend.common.utils.helper import soft_delete_model_instance
from recipe_house_backend.common.utils.permissions import IsOwnerOrReadOnly


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

class PostTypeViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Cuisine
    """
    queryset = PostType.objects.get_all_active()
    serializer_class = PostTypeSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PostTypeUpdateSerializer
        return self.serializer_class


class PostViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Post
    """
    queryset = Post.objects.get_by_filter()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'cuisine__name','tags')
    serializer_action_classes = {
        'list': PostListAdminSerializer,
        'post': PostSerializer,
        'retrieve': PostDetailsSerializer

    }

    def perform_destroy(self, instance):
        soft_delete_model_instance(instance, self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        post_type = self.request.query_params.get('post-type', None)
        cuisine = self.request.query_params.get('cuisine', None)
        created_by = self.request.query_params.get('created-by', None)
        if post_type:
            queryset = queryset.filter(post_type=post_type)
        if cuisine:
            queryset = queryset.filter(cuisine=cuisine)
        if created_by:
            queryset = queryset.filter(created_by=self.request.user)

        return queryset

class PostAddMasterData(APIView):
    def get(self, request):
        category = Category.objects.get_all_active()
        cuisine = Cuisine.objects.get_all_active()
        data = {
            'category': CategoryListSerializer(category, many=True).data,
            'cuisine': CuisineListSerializer(cuisine, many=True).data
        }
        return response_helper.http_200('Master data loaded', data)
