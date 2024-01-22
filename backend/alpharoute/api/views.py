from rest_framework import viewsets

from employee.models import CustomUser
from templatestask.models import Template

from .serializers import CustomUserListSerializer, TemplateSerializer


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
