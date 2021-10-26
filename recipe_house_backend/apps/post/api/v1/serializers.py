from rest_framework import serializers

from recipe_house_backend.apps.post.models import Tag, Post, Category, Cuisine


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """
    created_by_name = serializers.SerializerMethodField()

    class Meta(object):
        model = Tag
        fields = '__all__'

    def get_created_by_name(self, obj):
        return obj.created_by.email


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    created_by_name = serializers.SerializerMethodField()

    class Meta(object):
        model = Category
        fields = '__all__'

    def get_created_by_name(self, obj):
        return obj.created_by.email


class CuisineSerializer(serializers.ModelSerializer):
    """
    Serializer for Cuisine model
    """
    created_by_name = serializers.SerializerMethodField()

    class Meta(object):
        model = Cuisine
        fields = '__all__'

    def get_created_by_name(self, obj):
        return obj.created_by.email


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """

    class Meta(object):
        model = Post
        fields = '__all__'
