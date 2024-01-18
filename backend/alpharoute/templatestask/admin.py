from django.contrib import admin

from .models import Template


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    model = Template
    list_display = ('id', 'title', 'description', 'link_url')
    ordering = ('id',)
    search_fields = ('id',)
