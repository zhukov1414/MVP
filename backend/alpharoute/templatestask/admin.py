from django.contrib import admin

from .models import Department, Template


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'department')
    list_filter = ('title', 'department')
    search_fields = ('title', 'department')
    empty_value_display = '-пусто-'


admin.site.register(Department)
admin.site.register(Template, TemplateAdmin)
