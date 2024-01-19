from django.urls import include, path

from .views import CustomUserViewSet, IndividualDevelopmentPlanViewSet

from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register('employee', CustomUserViewSet, basename='employee')
router_v1.register('employee/individual-development-plan', IndividualDevelopmentPlanViewSet, basename='ipr')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
