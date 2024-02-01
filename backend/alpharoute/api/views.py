from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from djoser.views import UserViewSet
# from api.permissions import IsOwnerOrReadOnly
from users.models import CustomUser
from ipr.models import (Comment, IndividualDevelopmentPlan,
                        Task, StatusIpr, StatusTask)
from templatestask.models import Template

from .serializers import (CommentSerializer,
                          CustomUserCreateSerializer,
                          CustomUserPageSerializer,
                          CustomUserListSerializer,
                          CustomUserSerializer,
                          IndividualDevelopmentPlanCreateSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                          TaskSerializer, TemplateSerializer)


class CustomUserViewSet(UserViewSet):
    """Управление пользователями."""

    queryset = CustomUser.objects.select_related('manager')
    permission_classes=[IsAuthenticated,]
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

    # @action(
    #     detail=True,
    #     methods=['POST', 'Delete', 'patch', ],
    #     url_path='ipr',
    #     permission_classes=[IsAuthenticated])
    # def get_ipr(self, request, id):
    #     """создать ипр, если его нет."""
        
        
    #     employee = get_object_or_404(CustomUser, id=id)
    #     # data = request.data
    #     data={'employee': employee,},
    #     serializer = IndividualDevelopmentPlanCreateSerializer(
    #         employee)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(f'создан ипр для {employee}',
    #                     status=status.HTTP_201_CREATED)

    # @ipr.mapping.delete
    # def ipr_delete(self, request, id):
    #     """Удалить ипр."""
    #     get_object_or_404(IndividualDevelopmentPlan,
    #                       employee_id=id).delete()
    #     return Response('ИПР удален',
    #                     status=status.HTTP_204_NO_CONTENT)



# class TemplateViewSet(viewsets.ModelViewSet):
#     queryset = Template.objects.all()
#     serializer_class = TemplateSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    methods=['get', 'post',],

    def perform_create(self, serializer):
        ipr = get_object_or_404(IndividualDevelopmentPlan,
                                id=self.kwargs.get('ipr_id'))
        serializer.save(ipr=ipr)


class IndividualDevelopmentPlanViewSet(viewsets.ModelViewSet):
    """ВьюСет для всего ИПР."""

    queryset = IndividualDevelopmentPlan.objects.select_related('employee')
    # queryset = get_object_or_404(IndividualDevelopmentPlan, id=self.kwargs.get('ipr_id'))
    permission_classes = (AllowAny,)
    
    # def get_queryset(self):
    #     ipr = get_object_or_404(IndividualDevelopmentPlan, 
    #                             employee=self.kwargs.get('id'))
    #     return ipr


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
        конртетному ипр"""
        comments = Comment.objects.filter(
            task__ipr__id=pk)
        if comments:
            serializer = CommentSerializer(
                comments, many=True,
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Комментариев пока нет',
                        status=status.HTTP_400_BAD_REQUEST)

    # @action(
    #     detail=True,
    #     # methods=['get', 'post', 'put', 'delete'],
    #     methods=['get',],
    #     permission_classes=[IsAuthenticated])
    # def get_task(self, request, pk=id):
    #     """Посмотреть конкретную задачу"""
    #     task = get_object_or_404(Task, id=self.request.id)
    #     # Comment.objects.filter(
    #     #     task__ipr__id=pk)
    #     # if comments:
    #     #     serializer = CommentSerializer(
    #     #         comments, many=True,
    #     #         context={'request': request})
    #     #     return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response('Комментариев пока нет',
    #                     status=status.HTTP_400_BAD_REQUEST)
    
