from rest_framework import serializers

from recipe_house_backend.apps.post.models import Tag, Post, Category, Cuisine


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """

    class Meta(object):
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """

    class Meta(object):
        model = Category
        fields = '__all__'


class CuisineSerializer(serializers.ModelSerializer):
    """
    Serializer for Cuisine model
    """

    class Meta(object):
        model = Cuisine
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """

    class Meta(object):
        model = Post
        fields = '__all__'
