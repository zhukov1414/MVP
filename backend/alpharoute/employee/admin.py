from django.contrib import admin

from .models import Employee, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role')
    list_filter = ('username', 'email', 'role')
    search_fields = ('username',)
    empty_value_display = '-пусто-'


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position',)
    list_filter = ('user',)
    search_fields = ('user',)
    empty_value_display = '-пусто-'


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
