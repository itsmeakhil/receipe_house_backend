from rest_framework import serializers

from recipe_house_backend.apps.favourites.models import FavouritePost
from recipe_house_backend.apps.post.api.v1.serializers import PostListSerializer


class FavouritePostSerializer(serializers.ModelSerializer):
    """
    Serializer for FavouritePost model
    """

    class Meta(object):
        model = FavouritePost
        fields = '__all__'

class FavouritePostListSerializer(serializers.ModelSerializer):
    """
    Serializer for FavouritePost model
    """
    post = PostListSerializer()
    class Meta(object):
        model = FavouritePost
        fields = '__all__'
