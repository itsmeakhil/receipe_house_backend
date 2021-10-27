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

    def validate(self, data):
        """Function to validate tag exists """
        if Tag.objects.does_exist(name=data['name']):
            raise serializers.ValidationError('Tag already exists')
        return data


class TagUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """

    class Meta(object):
        model = Tag
        fields = '__all__'


class TagNameSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """

    class Meta(object):
        model = Tag
        fields = ('name',)


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

    def validate(self, data):
        """Function to validate Category exists """
        if Category.objects.does_exist(name=data['name']):
            raise serializers.ValidationError('Category already exists')
        return data


class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """

    class Meta(object):
        model = Category
        fields = '__all__'


class CategoryNameSerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """

    class Meta(object):
        model = Category
        fields = ('name',)


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

    def validate(self, data):
        """Function to validate Cuisine exists """
        if Cuisine.objects.does_exist(name=data['name']):
            raise serializers.ValidationError('Cuisine already exists')
        return data


class CuisineUpdateSerializer(serializers.ModelSerializer):
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
    created_by_name = serializers.SerializerMethodField()

    class Meta(object):
        model = Post
        fields = '__all__'

    def get_created_by_name(self, obj):
        return obj.created_by.username


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """
    created_by_name = serializers.SerializerMethodField()
    cuisine_name = serializers.SerializerMethodField()
    tags = TagNameSerializer(many=True)
    category = CategoryNameSerializer(many=True)

    class Meta(object):
        model = Post
        fields = '__all__'

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def get_cuisine_name(self, obj):
        return obj.cuisine.name
