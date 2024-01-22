from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet, CustomUserViewSet,
                    IndividualDevelopmentPlanViewSet, TaskViewSet)
from .views import CustomUserViewSet, TemplateViewSet

app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register('employee', CustomUserViewSet, basename='employee')
router_v1.register('templates', TemplateViewSet, basename='templates')
router_v1.register('individual-development-plan',
                   IndividualDevelopmentPlanViewSet, basename='ipr')
router_v1.register('tasks', TaskViewSet, basename='task')
router_v1.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
