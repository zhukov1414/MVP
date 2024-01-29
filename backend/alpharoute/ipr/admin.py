from django.contrib import admin

from ipr import models


class TaskInline(admin.TabularInline):
    model = models.Task
    extra = 0


class IndividualDevelopmentPlanAdmin(admin.ModelAdmin):

    list_display = ('title',
                    'employee',
                    'goal',
                    'description',
                    'deadline',
                    )
    empty_value_display = '-пусто-'
    inlines = [TaskInline, ]


class TaskAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'deadline', 'status')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):

    list_display = ('author', 'task', 'postdate')
    empty_value_display = '-пусто-'


admin.site.register(models.IndividualDevelopmentPlan,
                    IndividualDevelopmentPlanAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Task, TaskAdmin)
