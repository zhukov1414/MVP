from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from employee.models import EmployeeCustomUser


@admin.register(EmployeeCustomUser)
class EmployeeCustomUserAdmin(UserAdmin):
    model = EmployeeCustomUser
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'password')
    ordering = ('username',)
    search_fields = ('first_name',)
