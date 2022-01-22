from rest_framework import serializers

from recipe_house_backend.apps.rating.models import Rating, Comment


class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for Rating model
    """

    class Meta(object):
        model = Rating
        fields = '__all__'

    def validate(self, data):
        """Function to validate Rating exists """
        if Rating.objects.does_exist(created_by=self.context['request'].user):
            raise serializers.ValidationError('You have already rated the recipe')
        return data


class RatingUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Rating model
    """

    class Meta(object):
        model = Rating
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """

    class Meta(object):
        model = Comment
        fields = '__all__'

    def validate(self, data):
        """Function to validate Comment exists """
        if Comment.objects.does_exist(created_by=self.context['request'].user):
            raise serializers.ValidationError('You have already commented the recipe')
        return data

class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """

    class Meta(object):
        model = Comment
        fields = '__all__'



