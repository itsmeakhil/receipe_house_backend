from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers, validators

from recipe_house_backend.apps.users.models import (
    User,
    Role
)
from recipe_house_backend.common.utils.helper import (
    decode_uid,
    check_user_token
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
        fields = ('url',
                  'id',
                  'email',
                  'first_name',
                  'last_name',
                  'role',
                  'password',
                  'date_joined',
                  'is_active',
                  'is_verified'
                  )
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
            roles = validated_data.pop('roles')
            user = super(UserSerializer, self).create(validated_data)
            if 'password' in validated_data:
                user.set_password(validated_data['password'])
            for role in roles:
                user.roles.add(role.id)

            user.save()
            return user

    def update(self, instance, validated_data):
        """
        Update User Model instance
        """
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']

        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']

        if 'role' in validated_data:
            instance.role=validated_data['role']
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
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_verified'
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):

        user = User.objects.filter(email=attrs['email']).first()
        if user:
            attrs['user'] = user
        else:
            raise serializers.ValidationError({"email": ["No user associated with this email"]})

        return attrs


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=3)
    confirm_password = serializers.CharField(min_length=3)
    uid = serializers.CharField(min_length=1)
    token = serializers.CharField(min_length=1)

    def validate(self, attrs):

        validated_data = super().validate(attrs)

        if validated_data['password'] != validated_data['confirm_password']:
            key_error = "password_mismatch"
            raise ValidationError(
                {"password": ["`password`, `confirm_password` is not matching"]}, code=key_error
            )

        try:
            uid = decode_uid(self.initial_data.get("uid", ""))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": ["invalid uid"]}, code=key_error
            )

        is_token_valid = check_user_token(user, self.initial_data.get("token", ""))
        if is_token_valid:

            # set password
            user.set_password(attrs['password'])
            user.save()

            return validated_data
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": ["invalid token"]}, code=key_error
            )
        pass


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=3)
    new_password = serializers.CharField(min_length=3)
    confirm_password = serializers.CharField(min_length=3)
