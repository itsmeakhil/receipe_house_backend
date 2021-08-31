from rest_framework import serializers

from recipe_house_backend.apps.blog.models import Tag, Blog


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """

    class Meta(object):
        model = Tag
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """

    class Meta(object):
        model = Blog
        fields = '__all__'


