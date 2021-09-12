from rest_framework import serializers

from recipe_house_backend.apps.blog.models import Tag, Blog, Category, Cuisine


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


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """

    class Meta(object):
        model = Blog
        fields = '__all__'
