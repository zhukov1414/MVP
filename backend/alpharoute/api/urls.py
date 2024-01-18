from django.urls import include, path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
# router_v1.register('employee',)
# router_v1.register('templates',)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
