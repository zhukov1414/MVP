from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsOwnerOrReadOnly
from employee.models import CustomUser
from ipr.models import Comment, IndividualDevelopmentPlan, Task
from templatestask.models import Template

from .serializers import (CommentSerializer, CustomUserCreateSerializer,
                          CustomUserListSerializer, CustomUserSerializer,
                          IndividualDevelopmentPlanCreateSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                          TaskSerializer, TemplateSerializer)


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Просмотр информации о себе."""
        serializer = CustomUserSerializer(
            self.request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsOwnerOrReadOnly, )
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)
        # serializer.save(author=self.request.user)

    def get_queryset(self):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        return task.comments.all()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    def perform_create(self, serializer):
        ipr = get_object_or_404(IndividualDevelopmentPlan,
                                id=self.kwargs.get('ipr_id'))
        serializer.save(ipr=ipr)


class IndividualDevelopmentPlanViewSet(viewsets.ModelViewSet):
    """ВьюСет для всего ИПР."""

    queryset = IndividualDevelopmentPlan.objects.all()
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IndividualDevelopmentPlanShortSerializer
        return IndividualDevelopmentPlanCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()
