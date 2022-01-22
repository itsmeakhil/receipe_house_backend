from rest_framework import filters
from rest_framework import viewsets

from recipe_house_backend.apps.favourites.api.v1.serializers import FavouritePostSerializer, FavouritePostListSerializer
from recipe_house_backend.apps.favourites.models import FavouritePost
from recipe_house_backend.common.utils.permissions import IsOwnerOrReadOnly


class FavouritePostViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for FavouritePost
    """
    queryset = FavouritePost.objects.get_all_active()
    serializer_class = FavouritePostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    serializer_action_classes = {
        'list': FavouritePostListSerializer,
        'post': FavouritePostSerializer,

    }
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=self.request.user)
        return queryset

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return self.serializer_class
