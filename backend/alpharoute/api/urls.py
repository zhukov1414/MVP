from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet,
                    IndividualDevelopmentPlanViewSet,
                    TaskViewSet,)
                    #TemplateViewSet)

app_name = 'api'
router_v1 = DefaultRouter()

router_v1.register('employee', CustomUserViewSet, basename='employee')
# router_v1.register('templates', TemplateViewSet, basename='templates')
router_v1.register('ipr', IndividualDevelopmentPlanViewSet, basename='ipr')
# router_v1.register(r'employee/(?P<employee_id>\d+)/ipr/',
                #    IndividualDevelopmentPlanViewSet, basename='ipr')
router_v1.register('task', TaskViewSet, basename='task')
# router_v1.register(r'ipr/(?P<ipr_id>\d+)/tasks/(?P<task_id>\d+)/comment',
#                    CommentViewSet, basename='comment')
# router_v1.register('task', TaskViewSet, basename='task')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
