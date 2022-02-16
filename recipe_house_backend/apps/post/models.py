from django.db import models

from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils.base_manager import BaseManager


class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CATEGORY'
        indexes = [
            models.Index(fields=['name']),
        ]


class Cuisine(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CUISINE'
        indexes = [
            models.Index(fields=['name']),
        ]


class PostType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'POST_TYPE'
        indexes = [
            models.Index(fields=['name']),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TAG'
        indexes = [
            models.Index(fields=['name']),
        ]


class Post(models.Model):
    ENGLISH = 2
    MALAYALAM = 1
    LANGUAGE_CHOICE = (
        (ENGLISH, 'English'),
        (MALAYALAM, 'Malayalam')
    )

    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='media/images/post', null=True, blank=True)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    preparation_time = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    serves = models.IntegerField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL)
    post_type = models.ForeignKey(PostType, null=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    language = models.IntegerField(choices=LANGUAGE_CHOICE, default=MALAYALAM)
    views = models.PositiveIntegerField(null=True, blank=True)

    objects = BaseManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'POST'
        indexes = [
            models.Index(fields=['title', 'tags']),
        ]
