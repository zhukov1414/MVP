from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from users.models import CustomUser

from ipr.models import Comment, IndividualDevelopmentPlan, Task, Template

from datetime import date


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""
    photo = Base64ImageField()
    ipr = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'is_staff',
                  'position', 'photo', 'manager', 'ipr', )
        read_only_fields = ('id', 'position', 'photo')

    def get_ipr(self, obj):
        ipr = IndividualDevelopmentPlan.objects.filter(
            employee_id=obj).all()
        return IndividualDevelopmentPlanShortSerializer(ipr, many=True).data


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name',
                  'position', 'photo', 'manager', 'is_staff' )

        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')


class CustomUserInIprSerializer(serializers.ModelSerializer):
    """Просмотр пользователя из ипр (имя/должность/фото)."""

    photo = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('name', 'position', 'photo',)


class TemplateSerializer(serializers.ModelSerializer):
    """Сериализация для создания шаблона."""

    class Meta:
        model = Template
        fields = ('id', 'title', 'description', 'linkURL', 'department')


class CommentSerializer(serializers.ModelSerializer):
    """Cериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='name',
    )
    task = serializers.SlugRelatedField(
        read_only=True, slug_field='title',
    )

    class Meta:
        fields = ('id', 'content', 'author', 'task', 'postdate',)
        model = Comment

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class TaskSerializer(serializers.ModelSerializer):
    """Cериализатор для просмотра задач."""
    ipr = serializers.SlugRelatedField(
        read_only=True, slug_field='title',
    )
    comments = CommentSerializer(many=True, read_only=True)
    is_commented = serializers.SerializerMethodField()
    is_out_if_date = serializers.SerializerMethodField()

    class Meta:
        model = Task
        read_only_fields = ('ipr',)
        fields = ('id', 'title', 'description', 'linkURL',
                  'ipr', 'deadline', 'status',
                  'is_commented', 'is_out_if_date', 'comments',
                  )

    def get_is_commented(self, obj):
        return Comment.objects.filter(
            task=obj).exists()

    def get_comments(self, obj):
        tasks = Task.objects.filter(ipr=obj)
        return TaskSerializer(tasks, many=True).data

    def get_is_out_if_date(self, obj,):
        now = date.today()
        if now > obj.deadline and obj.status != 'done':
            return True
        return False


class TaskChangeSerializer(serializers.ModelSerializer):
    """Cериализатор для создания и редактирования задач."""

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'linkURL',
                  'deadline', 'status', )

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, task, validated_data):
        return super().update(task, validated_data)


class IndividualDevelopmentPlanShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ИПР на странице сотрудника."""
    task = TaskSerializer(many=True, required=True,)
    progress = serializers.SerializerMethodField()
    is_out_if_date = serializers.SerializerMethodField()
    is_commented = serializers.SerializerMethodField()
    employee = CustomUserInIprSerializer()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('employee',
                  'id',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'is_out_if_date',
                  'is_commented',
                  'progress',
                  'task',
                  )

    def get_tasks(self, obj):
        tasks = Task.objects.filter(ipr=obj)
        return TaskSerializer(tasks, many=True).data

    def get_progress(self, obj):
        tasks = Task.objects.filter(ipr=obj).count()
        done_tasks = Task.objects.filter(ipr=obj, status='done').count()
        if done_tasks > 0:
            return int(done_tasks/tasks*100)
        return 0

    def get_is_out_if_date(self, obj,):
        now = date.today()
        bad_status = ('created', 'inwork')
        tasks = Task.objects.filter(ipr=obj)

        if now > obj.deadline and obj.status in bad_status:
            return True

        for task in tasks:
            if now > task.deadline and task.status != 'done':
                return True
        return False

    def get_is_commented(self, obj,):
        tasks = Task.objects.filter(ipr=obj)
        for task in tasks:
            if Comment.objects.filter(task=task).exists():
                return True
        return False


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
                  'status',
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
