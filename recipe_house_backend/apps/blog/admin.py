from django.contrib import admin

# Register your models here.
from recipe_house_backend.apps.blog.models import Cuisine, Blog, Tag, Category

class CuisineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


admin.site.register(Cuisine,CuisineAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Blog)
admin.site.register(Tag,TagAdmin)
