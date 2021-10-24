from rest_framework import serializers

from recipe_house_backend.apps.favourites.models import FavouritePost


class FavouritePostSerializer(serializers.ModelSerializer):
    """
    Serializer for FavouritePost model
    """

    class Meta(object):
        model = FavouritePost
        fields = '__all__'
