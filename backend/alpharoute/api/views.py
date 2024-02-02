from rest_framework import status, viewsets
from rest_framework.decorators import api_view,  permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.models import CustomUser
from ipr.models import (Comment, IndividualDevelopmentPlan,
                        Task)
from templatestask.models import Template

from .serializers import (CommentSerializer,
                          CustomAlliprListSerializer,
                          CustomUserWithoutIprSerializer,
                          CustomUserListSerializer,
                          IndividualDevelopmentPlanSerializer,
                          IndividualDevelopmentPlanShortSerializer,
                          TaskSerializer, TemplateSerializer)


class TemplateViewSet(viewsets.ModelViewSet):
    """Получаем все шаблоны включая по id"""
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def is_superuser(request):
    user = request.user
    is_super_user = user.is_superuser
    return Response({"is_superuser": is_super_user}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_all_users(request):
    users = CustomUser.objects.all()
    serializer = CustomUserListSerializer(users, many=True)
    return Response(serializer.data,
                    status=status.HTTP_200_OK)


@api_view(["GET"])  # Получаем всех сотрудников c ипр и без
def get_all_users_and_ipr(request):
    users_with_ipr = IndividualDevelopmentPlan.objects.all()
    users_without_ipr = CustomUserWithoutIprSerializer.get_users_without_ipr()

    serializer_with_ipr = CustomAlliprListSerializer(users_with_ipr,
                                                     many=True)
    serializer_without_ipr = CustomUserWithoutIprSerializer(users_without_ipr,
                                                            many=True)

    response_data = {
        "with_ipr": serializer_with_ipr.data,
        "without_ipr": serializer_without_ipr.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_all_ipr_users(request):
    employee = IndividualDevelopmentPlan.objects.all()
    serializer = CustomAlliprListSerializer(employee, many=True)
    return Response(serializer.data,
                    status=status.HTTP_200_OK)


@api_view(["GET"])
def get_user_by_id(request, id):
    try:
        user = CustomUser.objects.get(id=id)
        serializer = CustomUserListSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "Пользоваетль не найден"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])  # Получаем ИПР по emploee_id
def get_individual_development_plans_for_employee(request, employee_id):
    try:
        individual_development_plans = IndividualDevelopmentPlan.objects.filter(employee_id=employee_id)  # noqa: E501
        serializer = IndividualDevelopmentPlanShortSerializer(
            individual_development_plans,
            many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except IndividualDevelopmentPlan.DoesNotExist:
        return Response({"error":
                         "Индивидуальный план не найден у сотрудника"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])  # Создаем индивидуальный план по employee_id
def create_individual_development_plan(request, employee_id):
    try:
        plan_data = {
            'employeeId': employee_id,
            'goal': request.data.get('goal', ''),
            'deadline': request.data.get('deadline', ''),
            'status': request.data.get('status', ''),
            'tasks': request.data.get('tasks', []),
        }

        serializer = IndividualDevelopmentPlanSerializer(data=plan_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except CustomUser.DoesNotExist:
        return Response({"error": "Сотрудник не найден"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])  # Обновляем индивидуальный план по employee_id
def update_individual_development_plan(request, employee_id):
    try:
        plan = IndividualDevelopmentPlan.objects.get(employee_id=employee_id)

        plan_data = {
            'employeeId': employee_id,
            'goal': request.data.get('goal', plan.goal),
            'deadline': request.data.get('deadline', plan.deadline),
            'status': request.data.get('status', plan.status),
            'tasks': request.data.get('tasks', []),
        }
        serializer = IndividualDevelopmentPlanSerializer(
            plan,
            data=plan_data,
            partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except IndividualDevelopmentPlan.DoesNotExist:
        return Response({"error": "Индивидуальный план не найден"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])  # Удаляем индивидуальный план по employee_id
def delete_individual_development_plan(request, employee_id):
    try:
        individual_development_plan = IndividualDevelopmentPlan.objects.get(
            employee_id=employee_id)
        individual_development_plan.delete()
        return Response({"success": "Индивидуальный план успешно удален"},
                        status=status.HTTP_204_NO_CONTENT)
    except IndividualDevelopmentPlan.DoesNotExist:
        return Response({"error": "Индивидуальный план не найден"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])  # Получаем задачи в ипр по employee_id и ipr_id
def get_ipr_tasks(request, employee_id, ipr_id):
    try:
        tasks = Task.objects.filter(ipr__employee_id=employee_id,
                                    ipr_id=ipr_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Задачи не найдены"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])  # Получить информацию о задаче в ИПР сотрудника
def get_ipr_task(request, employee_id, ipr_id, task_id):
    try:
        task = Task.objects.get(ipr__employee_id=employee_id,
                                ipr_id=ipr_id,
                                id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"error": "Задачи не найдены"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])  # Создаем задачу в ипр по employee_id и ipr_id
def create_ipr_task(request, employee_id, ipr_id):
    try:
        ipr = IndividualDevelopmentPlan.objects.get(employee=employee_id,
                                                    id=ipr_id)
        task_data = {
            'ipr': ipr,
            'title': request.data.get('title', ''),
            'description': request.data.get('description', ''),
            'deadline': request.data.get('deadline', ''),
        }

        serializer = TaskSerializer(data=task_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    except IndividualDevelopmentPlan.DoesNotExist:
        return Response({"error": "Индивидуальный план не найден"},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["PATCH"])  # Обновляем задачу в ипр по employee_id, ipr_id, task_id
def update_ipr_task(request, employee_id, ipr_id, task_id):
    try:
        task = Task.objects.get(ipr__employee_id=employee_id,
                                ipr_id=ipr_id,
                                id=task_id)
        serializer = TaskSerializer(instance=task,
                                    data=request.data,
                                    partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    except Task.DoesNotExist:
        return Response({"error": "Задача не найдена"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])  # Удаляем задачу в ипр по employee_id, ipr_id, task_id
def delete_ipr_task(request, employee_id, ipr_id, task_id):
    try:
        task = Task.objects.get(ipr__employee_id=employee_id,
                                ipr_id=ipr_id, id=task_id)
        task.delete()
        return Response({"success": "Задача успешно удалена"},
                        status=status.HTTP_204_NO_CONTENT)
    except Task.DoesNotExist:
        return Response({"error": "Задача не найдена"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])  # Добавить комментарий к задаче в ИПР сотрудника
def create_task_comment(request, employee_id, ipr_id, task_id):
    try:
        task = Task.objects.get(
            ipr__employee_id=employee_id,
            ipr_id=ipr_id,
            id=task_id)
    except Task.DoesNotExist:
        return Response({"error": "Задача не найдена"},
                        status=status.HTTP_404_NOT_FOUND)

    comment_data = {
        'content': request.data.get('content', ''),
        'postdate': request.data.get('postdate', ''),
        'task': task.id,
    }

    comment_serializer = CommentSerializer(data=comment_data)
    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response(comment_serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response(comment_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])  # Получить комментарий к задаче в ИПР сотрудника
def get_task_comments(request, employee_id, ipr_id, task_id):
    try:
        comments = Comment.objects.filter(tasks_comments=task_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Comment.DoesNotExist:
        return Response({"error": "Комментарии не найдены"},
                        status=status.HTTP_404_NOT_FOUND)
