from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from employee.models import CustomUser
#from ipr.constants import STATUS_IPR, STATUS_TASK
from ipr.models import Comment, IndividualDevelopmentPlan, Task, StatusTask
from templatestask.models import Department, Template


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""

    image = Base64ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'image',
                  'first_name', 'last_name', 'position', )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    image = Base64ImageField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'image',
                  'first_name', 'last_name', 'password', )
        
        # def create(self, validated_data):
        #     return CustomUser.objects.create_user(
        #    validated_data['username'],
        #    None,
        #    validated_data['password'])


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей."""

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'first_name', 'last_name', 'position', 'image')
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
        read_only=True, slug_field='username',
    )
    # author = CustomUserSerializer(read_only=True)

    class Meta:
        fields = ('content', 'author', 'task', 'postdate')
        read_only_fields = ('post',)
        model = Comment


class TaskSerializer(serializers.ModelSerializer):
    """Cериализатор для задач."""
    
    # ipr = serializers.SlugRelatedField(
    #     read_only=True, slug_field='title',
    # )
    comments = CommentSerializer(many=True, read_only=True)
    is_commented = serializers.SerializerMethodField()

    class Meta:
        model = Task
        read_only_fields = ('ipr',)
        fields = ('title', 'description', 'linkURL',
                  'deadline', 'status', 'comments',
                  'is_commented')

    def get_is_commented(self, obj):
        return Comment.objects.filter(
            task=self.context.get('request').task).exists()

    # def create(self, validated_data):
    #     comments = validated_data.pop('comments')
    #     task = Task.objects.create(**validated_data)
    #     self.create_comments(comments, task)
    #     return task

    # def update(self, task, validated_data):
    #     Comment.objects.filter(task=task).all().delete()
    #     comments = validated_data.pop('comments')
    #     self.create_comments(comments, task)
    #     return super().update(task, validated_data)


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
    status = serializers.SerializerMethodField()
    status_percent = serializers.SerializerMethodField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'status',
                  'status_percent',
                  'task'
                  )

#    def get_status():
        


    def get_status_percent(self, obj):
        """Подсчет процента выполненных задач."""
        
        tasks = Task.objects.all()
        total_task = tasks.filter(id=obj.task).count()
        completed_task = tasks.filter(StatusTask.DONE).count()
        try:
            percent = (completed_task / total_task) * 100
        except ZeroDivisionError:
            return 0
        return percent


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

