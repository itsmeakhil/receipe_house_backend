# Create your models here.
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
# Model to Store Mission Problem Types
from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils.base_manager import BaseManager


class BlogType(models.Model):
    TRAVEL = 1
    CINEMA = 2
    FOOD_RECIPE = 3
    TECH = 4
    HEALTH = 5

    BLOG_TYPE_CHOICES = (
        (TRAVEL, 'Travel'),
        (CINEMA, 'Cinema'),
        (FOOD_RECIPE, 'Food Recipe'),
        (TECH, 'Tech'),
        (HEALTH, 'Health'),
    )
    id = models.PositiveSmallIntegerField(choices=BLOG_TYPE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


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
    ingredients = ArrayField(models.CharField(max_length=255, null=True, blank=True),null=True,blank=True)
    preparation = ArrayField(models.TextField(max_length=2000, null=True, blank=True),null=True,blank=True)
    serves = models.IntegerField(null=True, blank=True)
    type = models.ForeignKey(BlogType, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    is_deleted = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL),
    language = models.IntegerField(choices=LANGUAGE_CHOICE, default=MALAYALAM)

    objects = BaseManager()

    def __str__(self):
        return self.title
