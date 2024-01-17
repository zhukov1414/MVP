from djoser.serializers import UserCreateSerializer, UserSerializer

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
