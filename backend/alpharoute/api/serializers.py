from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers

from employee.models import CustomUser
from templatestask.models import Department, Template


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username',
                  'first_name', 'last_name', 'password',  'photo')


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username',
                  'first_name', 'last_name', 'password',  'photo')


class CustomUserListSerializer(serializers.ModelSerializer):
    """Сериализация списка пользователей."""

    photo = Base64ImageField()

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'first_name', 'last_name', 'position', 'photo')
        read_only_fields = ('id', 'name', 'first_name',
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
