from rest_framework import filters
from rest_framework import viewsets

from recipe_house_backend.apps.favourites.api.v1.serializers import FavouritePostSerializer
from recipe_house_backend.apps.favourites.models import FavouritePost


class FavouritePostViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for FavouritePost
    """
    queryset = FavouritePost.objects.get_all_active()
    serializer_class = FavouritePostSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options', 'put']
    filter_backends = (filters.SearchFilter,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
