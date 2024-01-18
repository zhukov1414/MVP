from django.contrib import admin

from .models import Comment, IndividualDevelopmentPlan, Task


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ('id', 'author', 'content', 'postdate')
    ordering = ('id',)
    search_fields = ('id',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('id', 'title', 'deadline', 'status')
    ordering = ('id',)
    search_fields = ('id',)


@admin.register(IndividualDevelopmentPlan)
class IndividualDevelopmentPlanAdmin(admin.ModelAdmin):
    model = IndividualDevelopmentPlan
    list_display = ('id', 'employee', 'goal', 'deadline', 'status')
    ordering = ('id',)
    search_fields = ('id',)
