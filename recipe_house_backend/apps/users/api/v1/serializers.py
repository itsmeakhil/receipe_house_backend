from django.db import transaction
from rest_framework import serializers, validators

from recipe_house_backend.apps.users.models import (
    User
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    email = serializers.EmailField(required=True,
                                   validators=[validators.UniqueValidator(
                                       queryset=User.objects.all())])

    class Meta(object):
        model = User
        fields = '__all__'
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'is_active': {'read_only': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Saves a User with email and password.
        """
        with transaction.atomic():
            user = super(UserSerializer, self).create(validated_data)
            if 'password' in validated_data:
                user.set_password(validated_data['password'])
            user.save()
            return user

    def update(self, instance, validated_data):
        """
        Update User Model instance
        """
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()

        return instance


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta(object):
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=3)
    new_password = serializers.CharField(min_length=3)
    confirm_password = serializers.CharField(min_length=3)
