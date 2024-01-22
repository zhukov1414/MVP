from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from employee.models import CustomUser
from templatestask.models import Department, Template
from ipr.models import Comment, IndividualDevelopmentPlan, Task


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username',
                  'first_name', 'last_name', 'position', )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username',
                  'first_name', 'last_name', 'password', )


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей."""

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'first_name', 'last_name', 'position',)
        read_only_fields = ('id', 'name', 'first_name',
                            'last_name', 'position',)


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
        read_only=True, slug_field='name',
    )
    # task = serializers.SlugRelatedField(
    #     read_only=True, slug_field='title',
    # )

    class Meta:
        fields = ('content', 'author', 'task', 'postdate')
        # read_only_fields = ('task',)
        model = Comment


class TaskSerializer(serializers.ModelSerializer):
    """Cериализатор для задач."""
    ipr = serializers.SlugRelatedField(
        read_only=True, slug_field='title',
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        read_only_fields = ('ipr',)
        fields = ('title', 'description', 'linkURL',
                  'ipr', 'deadline', 'status', 'comments')

    def create_comments(self, comments, task):
        Comment.objects.bulk_create([
            Comment(
                task=task, author=comment['author'],
                postdate=comment['postdate'],
                content=comment['content'])for comment in comments])

    def create(self, validated_data):
        comments = validated_data.pop('comments')
        task = Task.objects.create(**validated_data)
        self.create_comments(comments, task)
        return task

    def update(self, task, validated_data):
        Comment.objects.filter(task=task).all().delete()
        comments = validated_data.pop('comments')
        self.create_comments(comments, task)
        return super().update(task, validated_data)


class IndividualDevelopmentPlanShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ИПР."""
    task = TaskSerializer(many=True, required=True,)
    employee = CustomUserSerializer(read_only=True)

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


class IndividualDevelopmentPlanCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования ИПР."""
    task = TaskSerializer(many=True, required=True,)
    employee = serializers.SlugRelatedField(
        read_only=True, slug_field='username',)

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
