from employee.models import CustomUser
from .serializers import CustomUserListSerializer
from rest_framework import viewsets


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer
