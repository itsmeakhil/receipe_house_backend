from django.contrib import admin

# Register your models here.
from recipe_house_backend.apps.blog.models import BlogType, Blog, Tag

admin.site.register(BlogType)
admin.site.register(Blog)
admin.site.register(Tag)
