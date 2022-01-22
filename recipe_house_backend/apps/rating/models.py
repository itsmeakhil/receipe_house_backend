from django.db import models

from recipe_house_backend.apps.post.models import Post
from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils.base_manager import BaseManager


class Comment(models.Model):
    text = models.TextField(null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'POST_COMMENT'


class Rating(models.Model):
    value = models.IntegerField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    objects = BaseManager()

    def __str__(self):
        return self.value

    class Meta:
        db_table = 'POST_RATING'


