# Create your models here.
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.db import models

from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils.base_manager import BaseManager


class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CATEGORY'


class Cuisine(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CUISINE'


class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    objects = BaseManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TAG'


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
    ingredients = ArrayField(JSONField(default=dict, null=True, blank=True), null=True, blank=True)
    preparation = ArrayField(JSONField(null=True, blank=True, default=dict), null=True, blank=True)
    serves = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL),
    language = models.IntegerField(choices=LANGUAGE_CHOICE, default=MALAYALAM)

    objects = BaseManager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'POST'
