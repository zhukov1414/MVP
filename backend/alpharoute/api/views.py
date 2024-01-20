from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from api.permissions import IsOwnerOrReadOnly
from employee.models import CustomUser
from ipr.models import Comment, IndividualDevelopmentPlan, Task

from .serializers import (CommentSerializer, CustomUserListSerializer,
                          IndividualDevelopmentPlanCreateSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                        #   IndividualDevelopmentPlanSerializer,
                          TaskSerializer)


class CustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserListSerializer


class CommentViewSet(viewsets.ModelViewSet):
    # permission_classes = (AllowAny, )
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)


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
    # serializer_class = IndividualDevelopmentPlanSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IndividualDevelopmentPlanShortSerializer
        return IndividualDevelopmentPlanCreateSerializer

    def perform_create(self, serializer):
        # employee = get_object_or_404(CustomUser,
        #                              id=self.kwargs.get('employee_id'))
        serializer.save(employee=self.request.employee)

    def perform_update(self, serializer):
        serializer.save()
