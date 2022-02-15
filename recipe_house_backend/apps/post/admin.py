from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from recipe_house_backend.apps.post.models import Cuisine, Post, Tag, Category, PostType
from recipe_house_backend.apps.post.admin_resource import CategoryResource, TagResource, CuisineResource, \
    PostTypeResource


class CuisineAdmin(ImportExportModelAdmin):
    resource_class = CuisineResource
    search_fields = ('name',)
    list_filter=('created_by',)
    list_display = ('id', 'name',)


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    search_fields = ('name',)
    list_filter=('created_by',)
    list_display = ('id', 'name',)


class TagAdmin(ImportExportModelAdmin):
    resource_class = TagResource
    search_fields = ('name',)
    list_filter=('created_by',)
    list_display = ('id', 'name',)


class PostTypeAdmin(ImportExportModelAdmin):
    resource_class = PostTypeResource
    search_fields = ('name',)
    list_filter=('created_by',)
    list_display = ('id', 'name',)





class PostAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'created_at', 'is_published','created_by')



admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(PostType, PostTypeAdmin)
