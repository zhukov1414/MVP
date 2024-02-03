from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet,
                    IndividualDevelopmentPlanViewSet,
                    TaskViewSet,
                    CommentViewSet,
                    TemplateViewSet,
                    MainViewSet)

app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register('main', MainViewSet, basename='main')
router_v1.register('employee', CustomUserViewSet, basename='employee')
router_v1.register('templates', TemplateViewSet, basename='templates')
router_v1.register('ipr', IndividualDevelopmentPlanViewSet, basename='ipr')
router_v1.register(r'ipr/(?P<ipr_id>\d+)/tasks', TaskViewSet, basename='task')
router_v1.register(r'ipr/(?P<ipr_id>\d+)/tasks/(?P<task_id>\d+)/comment',
                   CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
