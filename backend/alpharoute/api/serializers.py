from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from employee.models import CustomUser
from ipr.models import IndividualDevelopmentPlan


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


class IndividualDevelopmentPlanCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ИПР."""

    employee = CustomUserSerializer(read_only=True)
    title = serializers.CharField(max_length=255,)
    goal = serializers.CharField(max_length=255,)
    deadline = serializers.DateField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  )


class IndividualDevelopmentPlanShortSerializer(IndividualDevelopmentPlanCreateSerializer):
    """Сериализатор для получения созданного ИПР."""

    employee = CustomUserSerializer(read_only=True)
    title = serializers.CharField(max_length=255,)
    goal = serializers.CharField(max_length=255,)
    deadline = serializers.DateField()

    class Meta:
        model = IndividualDevelopmentPlan
        fields = ('id',
                  'employee',
                  'title',
                  'goal',
                  'description',
                  'deadline',
                  'task',
                  )
