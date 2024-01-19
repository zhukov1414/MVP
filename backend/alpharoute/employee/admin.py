from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'position')
    list_filter = ('username', 'email', 'position', 'is_staff')
    search_fields = ('username',)
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)