from rest_framework import viewsets
from recipe_house_backend.apps.rating.api.v1.serializers import RatingSerializer, RatingUpdateSerializer, \
    CommentUpdateSerializer
from recipe_house_backend.apps.rating.models import Comment, Rating
from recipe_house_backend.common.utils.permissions import IsOwnerOrReadOnly


class RatingViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for PostRating
    """
    queryset = Rating.objects.get_all_active()
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ['post', 'patch', 'put', 'destroy']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_context(self):
        context = super(RatingViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return RatingUpdateSerializer
        return self.serializer_class


class CommentViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet Class for Comment
    """
    queryset = Comment.objects.get_all_active()
    serializer_class = RatingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'put']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_serializer_context(self):
        context = super(CommentViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return CommentUpdateSerializer
        return self.serializer_class
