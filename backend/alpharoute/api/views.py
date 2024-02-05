from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ipr.models import Comment, IndividualDevelopmentPlan, Task, Template
from users.models import CustomUser

from .serializers import (CommentSerializer, CustomUserSerializer,
                          IndividualDevelopmentPlanCreateSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                          TaskChangeSerializer, TaskSerializer,
                          TemplateSerializer)


class CustomUserViewSet(UserViewSet):
    """Позволяет просматривать список всех пользователей,
    отдельного пользователя и список релевантных пользователей.
    Возможность регистрации в MVP не предусмотрена."""

    queryset = CustomUser.objects.select_related('manager')
    permission_classes = [IsAuthenticated, ]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('^name', '^position')
    ordering_fields = ('name', 'id', 'position')
    serializer_class = CustomUserSerializer
    http_method_names = ['get',]

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[IsAuthenticated,])
    def profile(self, request):
        """Просмотр информации о себе."""
        serializer = CustomUserSerializer(
            self.request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        url_path='my_employee',
        permission_classes=[IsAuthenticated,])
    def get_employee_list(self, request,):
        """Посмотреть список своих подчиненных с
        полной информацией об их ипр."""
        employees = CustomUser.objects.filter(
            manager=self.request.user).all()
        if employees:
            serializer = CustomUserSerializer(
                employees, many=True,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('У вас нет подчиненных',
                        status=status.HTTP_400_BAD_REQUEST)


class TemplateViewSet(viewsets.ModelViewSet):
    """Шаблоны задач. """
    http_method_names = ['get', 'post',]
    queryset = Template.objects.all()
    filter_backends = (SearchFilter,  DjangoFilterBackend,
                       OrderingFilter)
    search_fields = ('^title', '^description')
    ordering_fields = ('id', 'department', 'title')
    serializer_class = TemplateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Комментарии к задачам."""
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    ordering_fields = ('id', 'task', 'postdate')
    http_method_names = ['get', 'post',]

    def perform_create(self, serializer):
        task = get_object_or_404(Task, id=self.kwargs.get('task_id'))
        serializer.save(author=self.request.user, task=task)


class TaskViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с имеющимися задачами,
    и создания дополнительной в имеющемся ИПР."""
    queryset = Task.objects.select_related('ipr')
    filter_backends = (OrderingFilter, DjangoFilterBackend,)
    ordering_fields = ('id', 'status')

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
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('^employee_name', '^title')
    ordering_fields = (
        'employee_name',
        'title',
        "status",
        'deadline',
    )

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
        """Отдельно получить список комментариев к ИПР."""
        comments = Comment.objects.filter(
            task__ipr__id=pk)
        if comments:
            serializer = CommentSerializer(
                comments, many=True,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Комментариев пока нет',
                        status=status.HTTP_400_BAD_REQUEST)


class MainViewSet(viewsets.ModelViewSet):
    """Главная страница. Руководитель увидит список сотрудников,
    а линейный сотрудник -свою страницу."""
    http_method_names = ['get', ]
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
