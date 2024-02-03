from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'manager')
    list_filter = ('username', 'name')
    search_fields = ('username', 'name')
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
