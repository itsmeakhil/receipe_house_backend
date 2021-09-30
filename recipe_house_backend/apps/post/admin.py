from django.contrib import admin
from django.contrib.postgres.fields import ArrayField, JSONField
from django.forms.widgets import Textarea

from recipe_house_backend.apps.post.models import Cuisine, Post, Tag, Category


class CuisineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'preparation_time', 'serves', 'language', 'created_at', 'is_published')

    formfield_overrides = {
        JSONField: {'widget': Textarea(attrs={'rows': 30, 'cols': 100})},
        ArrayField: {'widget': Textarea(attrs={'rows': 10, 'cols': 50})},

    }


admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
