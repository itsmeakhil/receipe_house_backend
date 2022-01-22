from django.contrib import admin

from recipe_house_backend.apps.rating.models import Rating, Comment

admin.site.register(Rating)
admin.site.register(Comment)