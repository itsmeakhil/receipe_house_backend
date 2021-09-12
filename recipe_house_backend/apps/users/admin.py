from django.contrib import admin

from recipe_house_backend.apps.users.models import User, Role


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'is_verified',
                    'is_deleted', 'deleted_by', 'deleted_on')


admin.site.register(User, UserAdmin)
admin.site.register(Role)
