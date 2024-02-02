from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet
from users.models import CustomUser
from ipr.models import (Comment, IndividualDevelopmentPlan,
                        Task,)
from templatestask.models import Template

from .serializers import (CommentSerializer,
                          CustomUserListSerializer,
                          CustomUserSerializer,
                          IndividualDevelopmentPlanCreateSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                          TaskChangeSerializer,
                          TaskSerializer,
                          TemplateSerializer)


class CustomUserViewSet(UserViewSet):
    """Сериализатор позволяет просматривать список всех пользователей,
    отдельного пользователя и список релевантных пользователей."""

    queryset = CustomUser.objects.select_related('manager')
    permission_classes = [IsAuthenticated,]
    serializer_class = CustomUserListSerializer
    http_method_names = ['get',]

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

    @action(
        detail=False,
        methods=['get'],
        url_path='my_employee',
        permission_classes=[IsAuthenticated])
    def get_employee_list(self, request,):
        """Посмотреть список своих подчиненных с их ипр
        (без лишних полей)."""
        employees = CustomUser.objects.filter(
            manager=self.request.user).all()
        if employees:
            serializer = CustomUserListSerializer(
                employees, many=True,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('У вас нет подчиненных',
                        status=status.HTTP_400_BAD_REQUEST)


class TemplateViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post',]
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post',]

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)


class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с имеющимися задачами,
    и создания дополнительной в имеющемся ИПР."""
    # serializer_class = TaskChangeSerializer
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskSerializer
        return TaskChangeSerializer

    def perform_create(self, serializer):
        ipr = get_object_or_404(IndividualDevelopmentPlan,
                                id=self.kwargs.get('ipr_id'))
        serializer.save(ipr=ipr)


class IndividualDevelopmentPlanViewSet(viewsets.ModelViewSet):
    """ВьюСет для ИПР."""

    queryset = IndividualDevelopmentPlan.objects.all()
    permission_classes = (AllowAny,)
    methods = ['get', 'post', 'patch', 'delete'],

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return IndividualDevelopmentPlanShortSerializer
        return IndividualDevelopmentPlanCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    @action(
        detail=True,
        methods=['get'],
        permission_classes=[IsAuthenticated])
    def get_all_comments(self, request, pk=id):
        """Посмотреть все комментарии, привязанные к
        конкретному ипр."""
        comments = Comment.objects.filter(
            task__ipr__id=pk)
        if comments:
            serializer = CommentSerializer(
                comments, many=True,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Комментариев пока нет',
                        status=status.HTTP_400_BAD_REQUEST)
