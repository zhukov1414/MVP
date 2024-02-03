from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from users.models import CustomUser

from ipr.models import Comment, IndividualDevelopmentPlan, Task, Template
# from templatestask.models import Department, Template
from datetime import date


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'is_staff',
                  'position', 'photo', 'manager',)
        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'password', 'first_name',
                  'last_name', 'position', 'photo', 'manager')


class IndividualDevelopmentPlanIprSerializer(serializers.ModelSerializer):
    """Сериализатор для очень короткого отображения ипр в списке сотрудников
    (мало полей, но есть прогресс и указание на просроченность)."""

    is_out_if_date = serializers.SerializerMethodField()
    is_commented = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'title',
                  'deadline',
                  'is_out_if_date',
                  'is_commented',
                  'progress',
                  )

    def get_progress(self, obj):
        tasks = Task.objects.filter(ipr=obj).count()
        done_tasks = Task.objects.filter(ipr=obj, status='done').count()
        if done_tasks > 0:
            return round(done_tasks/tasks*100, 2)
        return 0  # получаем процент

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


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей без лишних полей."""

    photo = Base64ImageField()
    ipr = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'first_name', 'last_name',
                  'full_name',
                  'position', 'photo', 'ipr', )

        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')

    def get_ipr(self, obj):
        ipr = IndividualDevelopmentPlan.objects.filter(
            employee_id=obj).all()
        return IndividualDevelopmentPlanIprSerializer(ipr, many=True).data

    def get_full_name(self, obj):
        full_name = obj.last_name + ' ' + obj.name + ' ' + obj.first_name
        return full_name


class CustomUserInIprSerializer(serializers.ModelSerializer):
    """Просмотр пользователя из ипр (имя/должность/фото)."""

    photo = Base64ImageField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('name', 'first_name', 'last_name', 'full_name',
                  'position', 'photo',)

    def get_full_name(self, obj):
        full_name = obj.last_name + ' ' + obj.name + ' ' + obj.first_name
        return full_name


class TaskInIprSerializer(serializers.ModelSerializer):
    """Просмотр задачи в ипр."""

    is_commented = serializers.SerializerMethodField()

    class Meta:
        model = Task
        read_only_fields = ('ipr',)
        fields = ('id', 'title', 'description', 'status',
                  'deadline', 'is_commented')

    def get_is_commented(self, obj):
        return Comment.objects.filter(
            task=obj).exists()


class IndividualDevelopmentPlanShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ИПР на странице сотрудника."""
    task = TaskInIprSerializer(many=True, required=True,)
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
        return TaskInIprSerializer(tasks, many=True).data

    def get_progress(self, obj):
        tasks = Task.objects.filter(ipr=obj).count()
        done_tasks = Task.objects.filter(ipr=obj, status='done').count()
        if done_tasks > 0:
            return round(done_tasks/tasks*100, 2)
        return 0  # получаем процент

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


# class DepartmentSerializer(serializers.ModelSerializer):
#     """Сериализация направления для шаблона."""

#     class Meta:
#         model = Department
#         fields = ('id', 'title')


class TemplateSerializer(serializers.ModelSerializer):
    """Сериализация для создания шаблона."""

    class Meta:
        model = Template
        fields = ('id', 'title', 'description', 'linkURL', 'department')


class CommentSerializer(serializers.ModelSerializer):
    """Cериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )
    task = serializers.SlugRelatedField(
        read_only=True, slug_field='title',
    )

    class Meta:
        fields = ('id', 'content', 'author', 'task', 'postdate')
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
                  'ipr', 'deadline', 'status', 'comments',
                  'is_commented', 'is_out_if_date')

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
