from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from employee.models import CustomUser


class CustomUserSerializer(UserSerializer):
    """Сериализатор для управления пользователями."""

    class Meta:
        model = CustomUser
        fields = ('id', 'username',
                  'first_name', 'last_name', 'password', )


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
        fields = ('id', 'username', 'first_name', 'last_name', 'position',)
        read_only_fields = ('username', 'first_name', 'last_name', 'position',)
