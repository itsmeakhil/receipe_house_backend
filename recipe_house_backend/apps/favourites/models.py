from django.db import models

from recipe_house_backend.apps.post.models import Post
from recipe_house_backend.apps.users.models import User
from recipe_house_backend.common.utils.base_manager import BaseManager


class FavouritePost(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.SET_NULL)
    is_deleted = models.BooleanField(default=False)

    objects = BaseManager()

    def __str__(self):
        return self.id.__str__()

    class Meta:
        db_table = 'FAVOURITE_POST'
