from rest_framework import serializers

from recipe_house_backend.apps.post.models import Tag, Post, Category, Cuisine, PostType


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """
    created_by_name = serializers.CharField(source= 'created_by.email')

    class Meta(object):
        model = Tag
        fields = '__all__'

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


class TagListSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model
    """

    class Meta(object):
        model = Tag
        fields = ('id', 'name')


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
    created_by_name = serializers.CharField(source= 'created_by.email')

    class Meta(object):
        model = Category
        fields = '__all__'


    def validate(self, data):
        """Function to validate Category exists """
        if Category.objects.does_exist(name=data['name']):
            raise serializers.ValidationError('Category already exists')
        return data


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """

    class Meta(object):
        model = Category
        fields = ('id', 'name')


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

class PostTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    created_by_name = serializers.CharField(source= 'created_by.email')

    class Meta(object):
        model = PostType
        fields = '__all__'


    def validate(self, data):
        """Function to validate Category exists """
        if PostType.objects.does_exist(name=data['name']):
            raise serializers.ValidationError('PostType already exists')
        return data


class PostTypeListSerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """

    class Meta(object):
        model = PostType
        fields = ('id', 'name')


class PostTypeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for PostType model
    """

    class Meta(object):
        model = PostType
        fields = '__all__'


class PostTypeNameSerializer(serializers.ModelSerializer):
    """
    Serializer for PostType model
    """

    class Meta(object):
        model = PostType
        fields = ('name',)


class CuisineSerializer(serializers.ModelSerializer):
    """
    Serializer for Cuisine model
    """
    created_by_name = serializers.CharField(source= 'created_by.email')

    class Meta(object):
        model = Cuisine
        fields = '__all__'



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


class CuisineListSerializer(serializers.ModelSerializer):
    """
    Serializer for Cuisine model
    """

    class Meta(object):
        model = Cuisine
        fields = ('id', 'name')


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """
    created_by_name = serializers.CharField(source= 'created_by.username')
    class Meta(object):
        model = Post
        fields = '__all__'



class PostListAdminSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """
    created_by_name = serializers.CharField(source= 'created_by.username')
    cuisine_name = serializers.CharField(source= 'cuisine.name')
    category = CategoryNameSerializer(many=True)

    class Meta(object):
        model = Post
        fields = '__all__'

    def get_created_by_name(self, obj):
        return obj.created_by.username

    def get_cuisine_name(self, obj):
        return obj.cuisine.name


class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model
    """
    created_by_name = serializers.CharField(source='created_by.username')
    rating = serializers.SerializerMethodField()

    class Meta(object):
        model = Post
        fields = ('id','title','created_by_name','image','rating')

    def get_rating(self, obj):
        return '4'

class PostDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog model

    """
    created_by_name = serializers.CharField(source='created_by.username')
    cuisine_name = serializers.CharField(source='cuisine.name')
    category = CategoryNameSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta(object):
        model = Post
        fields = '__all__'

    def get_rating(self, obj):
        return '4'