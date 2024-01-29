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
                  'position', 'photo', 'manager',)
        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'password', 'first_name',
                  'last_name', 'position', 'photo', 'manager')


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


class CommentSerializer(serializers.ModelSerializer):
    """Cериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    # author = CustomUserSerializer(read_only=True)

    class Meta:
        fields = ('content', 'author', 'task', 'postdate')
        read_only_fields = ('post',)
        model = Comment


class TaskSerializer(serializers.ModelSerializer):
    """Cериализатор для задач."""
    ipr = serializers.SlugRelatedField(
        read_only=True, slug_field='title',
    )
    comments = CommentSerializer(many=True, read_only=True)
    is_commented = serializers.SerializerMethodField()

    class Meta:
        model = Task
        read_only_fields = ('ipr',)
        fields = ('id', 'title', 'description', 'linkURL',
                  'ipr', 'deadline', 'status', 'comments',
                  'is_commented')

    def get_is_commented(self, obj):
        return Comment.objects.filter(
            task=obj).exists()

    def get_comments(self, obj):
        tasks = Task.objects.filter(ipt=obj)
        return TaskSerializer(tasks, many=True).data

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, task, validated_data):
        return super().update(task, validated_data)


class IndividualDevelopmentPlanShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ИПР."""
    task = TaskSerializer(many=True, required=True,)

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'task'
                  )

    def get_tasks(self, obj):
        tasks = Task.objects.filter(ipt=obj)
        return TaskSerializer(tasks, many=True).data


class IndividualDevelopmentPlanCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования ИПР (вместе с задачами)."""
    task = TaskSerializer(many=True, required=True,)

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'task'
                  )

    def validate(self, data):
        task = self.initial_data.get('task')
        if not task:
            raise serializers.ValidationError('Добавьте хотя бы одну задачу')
        return data

    def create_tasks(self, tasks, ipr):
        Task.objects.bulk_create([
            Task(
                ipr=ipr, title=task['title'],
                description=task['description'],
                linkURL=task['linkURL'],
                deadline=task['deadline'],
                status=task['status'])for task in tasks])

    def create(self, validated_data):
        tasks = validated_data.pop('task')
        ipr = IndividualDevelopmentPlan.objects.create(**validated_data)
        self.create_tasks(tasks, ipr)
        return ipr

    def update(self, ipr, validated_data):
        Task.objects.filter(ipr=ipr).all().delete()
        tasks = validated_data.pop('task')
        self.create_tasks(tasks, ipr)
        return super().update(ipr, validated_data)


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей."""

    photo = Base64ImageField()
    # ipr = IndividualDevelopmentPlanShortSerializer(many=True,)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'position', 'photo',
                  'manager', )#'ipr')

        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')

    # def get_ipr(self, obj):
    #     return IndividualDevelopmentPlan.objects.filter(
    #         employee=self.context['request'].user)
    
