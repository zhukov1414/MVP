from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    get_all_users,
    get_user_by_id,
    get_individual_development_plans_for_employee,
    create_individual_development_plan,
    update_individual_development_plan,
    delete_individual_development_plan,
    get_ipr_tasks,
    create_ipr_task,
    get_ipr_task,
    update_ipr_task,
    delete_ipr_task,
    create_task_comment,
    get_task_comments,
    is_superuser,
    get_all_ipr_users,
    get_all_users_and_ipr,
    TemplateViewSet,
)

app_name = "api"
router_v1 = DefaultRouter()

router_v1.register("templates", TemplateViewSet, basename="templates")


urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/is_superuser/", is_superuser, name="is_superuser"),
    path("v1/employee/", get_all_users, name="get_all_users"),
    path("v1/employee/get_all_users_and_ipr/",
         get_all_users_and_ipr, name="get_all_users_and_ipr"),
    path("v1/employee_get_ipr/", get_all_ipr_users, name="get_all_ipr_users"),
    path("v1/employee/<int:id>/", get_user_by_id, name="get_user_by_id"),
    path(
        "v1/employee/<int:employee_id>/individual-plan/",
        get_individual_development_plans_for_employee,
        name="get_individual_development_plans_for_employee",
    ),
    path(
        "v1/employee/<str:employee_id>/individual-plan/create/",
        create_individual_development_plan,
    ),
    path(
        "v1/employee/<str:employee_id>/individual-plan/update/",
        update_individual_development_plan,
    ),
    path(
        "v1/employee/<str:employee_id>/individual-plan/delete/",
        delete_individual_development_plan,
    ),
    path(
        "v1/employee/<int:employee_id>/individual-plan/<int:ipr_id>/tasks/",
        get_ipr_tasks,
        name="get_ipr_tasks",
    ),
    path(
        "v1/employee/<int:employee_id>/"
        "individual-plan/<int:ipr_id>/create-ipr-task/",
        create_ipr_task,
        name="create_ipr_task",
    ),
    path(
        "v1/employee/<int:employee_id>/"
        "individual-plan/<int:ipr_id>/tasks/<int:task_id>/",
        get_ipr_task,
        name="get_ipr_task",
    ),
    path(
        "v1/employee/<int:employee_id>/"
        "individual-plan/<int:ipr_id>/tasks/<int:task_id>/update/",
        update_ipr_task,
        name="update_ipr_task",
    ),
    path(
        "v1/employee/<int:employee_id>/"
        "individual-plan/<int:ipr_id>/tasks/<int:task_id>/delete/",
        delete_ipr_task,
        name="delete_ipr_task",
    ),
    path(
        "v1/employee/<int:employee_id>/"
        "individual-plan/<int:ipr_id>/tasks/<int:task_id>/comment/",
        create_task_comment,
        name="create_task_comment",
    ),
    path(
        "v1/employee/<int:employee_id>/"
        "individual-plan/<int:ipr_id>/tasks/<int:task_id>/get-comment-task/",
        get_task_comments,
        name="get_task_comments",
    ),
    path("auth/", include("djoser.urls.authtoken")),
]
