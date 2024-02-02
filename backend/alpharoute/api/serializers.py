from datetime import date
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from users.models import CustomUser

from ipr.models import Comment, IndividualDevelopmentPlan, Task
from templatestask.models import Department, Template


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'position', 'photo')
        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'password', 'first_name',
                  'last_name', 'position', 'photo')


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализация направления для шаблона."""

    class Meta:
        model = Department
        fields = ('id', 'title')


class TemplateSerializer(serializers.ModelSerializer):
    """Сериализация для создания шаблона."""

    class Meta:
        model = Template
        fields = ('id', 'title', 'description', 'linkURL', 'department')
        # шаблон привязан к направлению?


class CommentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('name', 'last_name')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'postdate')

    def get_author(self, obj):
        return {'name': obj.author.name, 'last_name': obj.author.last_name}


class TaskSerializer(serializers.ModelSerializer):

    has_comments = serializers.SerializerMethodField()
    comments = CommentSerializer()

    class Meta:
        model = Task
        fields = ('id',
                  'title',
                  'deadline',
                  'description',
                  'status',
                  'linkURL',
                  'has_comments',
                  'comments',
                  )

    def get_has_comments(self, obj):
        return obj.comments is not None


class IndividualDevelopmentPlanShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ИПР."""
    task = TaskSerializer(many=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'is_overdue',
                  'status',
                  'task',
                  )

    def get_is_overdue(self, obj):
        return obj.deadline < date.today()


class IndividualDevelopmentPlanSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления ИПР."""

    tasks = TaskSerializer(many=True)

    class Meta:
        model = IndividualDevelopmentPlan
        fields = '__all__'

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks', [])
        individual_development_plan = IndividualDevelopmentPlan.objects.create(**validated_data)  # noqa: E501

        for task_data in tasks_data:
            Task.objects.create(ipr=individual_development_plan, **task_data)

        return individual_development_plan


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей."""

    photo = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'position', 'photo')

        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')


class CustomUserWithoutIprSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей без ИПР."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'position', 'photo')

    @classmethod
    def get_users_without_ipr(cls):
        return cls.Meta.model.objects.filter(ipr_employee__isnull=True)


class CustomAlliprListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей с ипр."""

    employee = CustomUserSerializer()
    task = TaskSerializer(many=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'progress',
                  'description',
                  'deadline',
                  'is_overdue',
                  'status',
                  'task',
                  )

    def get_is_overdue(self, obj):
        return obj.deadline < date.today()


class CustomUserListResponseSerializer(serializers.Serializer):
    with_ipr = CustomAlliprListSerializer(many=True)
    without_ipr = CustomUserWithoutIprSerializer(many=True)
