from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, TemplateViewSet

router_v1 = DefaultRouter()
router_v1.register('employee', CustomUserViewSet, basename='employee')
router_v1.register('templates', TemplateViewSet, basename='templates')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
