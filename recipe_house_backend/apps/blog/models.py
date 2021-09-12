# Create your models here.
from django.contrib.postgres.fields import ArrayField
from django.db import models

from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils.base_manager import BaseManager
from django.contrib.postgres.fields import JSONField


class Category(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    objects = BaseManager()

    def __str__(self):
        return self.name


class Blog(models.Model):
    ENGLISH = 2
    MALAYALAM = 1
    LANGUAGE_CHOICE = (
        (ENGLISH, 'English'),
        (MALAYALAM, 'Malayalam')
    )
    title = models.CharField(max_length=255, null=True, blank=True)
    featured_image = models.URLField(max_length=500, null=True, blank=True)
    preparation_time = models.CharField(max_length=255, null=True, blank=True)
    ingredients = ArrayField(models.CharField(max_length=255, null=True, blank=True), null=True, blank=True)
    preparation = ArrayField(JSONField(null=True,blank=True), null=True, blank=True)
    serves = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL),
    language = models.IntegerField(choices=LANGUAGE_CHOICE, default=MALAYALAM)

    objects = BaseManager()

    def __str__(self):
        return self.title
