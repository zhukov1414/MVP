from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from users.models import CustomUser

from ipr.models import Comment, IndividualDevelopmentPlan, Task
from templatestask.models import Department, Template
from datetime import date


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


class IndividualDevelopmentPlanIprSerializer(serializers.ModelSerializer):
    """Сериализатор для очень короткого отображения ипр в списке сотрудников
    (мало полей, но есть прогресс и указание на просроченность)."""

    is_out_if_date = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'title',
                  'deadline',
                  'is_out_if_date',
                  'progress',
                  )

    def get_is_out_if_date(self, data):
        now = date.today()
        bad_status = ('created', 'inwork')

        if now > data.deadline and data.status in bad_status:
            return True
        return False

    def get_progress(self, obj):
        tasks = Task.objects.filter(ipr=obj).count()
        done_tasks = Task.objects.filter(ipr=obj, status='done').count()
        return round(done_tasks/tasks*100, 2)  # получаем процент


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей без лишних полей."""

    photo = Base64ImageField()
    ipr = serializers.SerializerMethodField()
    # ipr = IndividualDevelopmentPlanIprSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'first_name', 'last_name',
                  'position', 'photo', 'ipr', )

        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')

    def get_ipr(self, obj):
        ipr = IndividualDevelopmentPlan.objects.filter(
            employee_id=obj).all()
        return IndividualDevelopmentPlanIprSerializer(ipr, many=True).data


class CustomUserInIprSerializer(serializers.ModelSerializer):
    """Просмотр пользователя из ипр (имя/должность/фото)."""

    photo = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('name', 'first_name', 'last_name',
                  'position', 'photo',)


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
        tasks = Task.objects.filter(ipr=obj)
        return TaskSerializer(tasks, many=True).data

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, task, validated_data):
        return super().update(task, validated_data)

    # def get_tasks(self, obj):
    #     tasks = Task.objects.filter(ipt=obj)
    #     return TaskSerializer(tasks, many=True).data

    # def check_status(self, tasks):
    #     for task in tasks:
    #         if self.task.filter(status=StatusTask.INWORK).exists()


class TaskInIprSerializer(serializers.ModelSerializer):
    """Просмотр задачи в ипр."""

    is_commented = serializers.SerializerMethodField()

    class Meta:
        model = Task
        read_only_fields = ('ipr',)
        fields = ( 'title', 'description', 'status', 
                  'deadline', 'is_commented')

    def get_is_commented(self, obj):
        return Comment.objects.filter(
            task=obj).exists()


class IndividualDevelopmentPlanIprSerializer(serializers.ModelSerializer):
    """Сериализатор для очень короткого отображения ипр в списке сотрудников
    (мало полей, но есть прогресс и указание на просроченность)."""

    is_out_if_date = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'title',
                  'deadline',
                  'is_out_if_date',
                  'progress',
                  )

    def get_is_out_if_date(self, data):
        now = date.today()
        bad_status = ('created', 'inwork')

        if now > data.deadline and data.status in bad_status:
            return True
        return False

    def get_progress(self, obj):
        tasks = Task.objects.filter(ipr=obj).count()
        done_tasks = Task.objects.filter(ipr=obj, status='done').count()
        return round(done_tasks/tasks*100, 2)  # получаем процент


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


class IndividualDevelopmentPlanShortSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра ИПР на странице сотрудника."""
    task = TaskInIprSerializer(many=True, required=True,)
    progress = serializers.SerializerMethodField()
    # employee = CustomUserInIprSerializer()
    is_out_if_date = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = (#'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'is_out_if_date',
                  'progress',
                  'task',
                  )

    def get_tasks(self, obj):
        tasks = Task.objects.filter(ipr=obj)
        return TaskInIprSerializer(tasks, many=True).data

    def get_progress(self, obj):
        tasks = Task.objects.filter(ipr=obj).count()
        done_tasks = Task.objects.filter(ipr=obj, status='done').count()
        return round(done_tasks/tasks*100, 2)  # получаем процент

    def get_is_out_if_date(self, data):
        now = date.today()
        bad_status = ('created', 'inwork')

        if now > data.deadline and data.status in bad_status:
            return True
        return False


class CustomUserPageSerializer(UserSerializer):
    """Сериализатор для просмотра ИПР."""

    ipr = IndividualDevelopmentPlanShortSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'first_name', 'last_name',
                  'position', 'photo', 'manager',
                  'ipr')
        read_only_fields = ('id',  'first_name',
                            'last_name', 'position', 'photo')