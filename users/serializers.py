from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()
PASSWORD_ERROR = 'Пароли не совпадают, попробуйте еще раз'
USERNAME_UNIQUE = 'Данное имя пользователя уже занято'
EMAIL_UNIQUE = 'Этот email уже зарегестрирован'


class UserSerializerForAuth(serializers.Serializer):
    """Сериализатор для регистрации."""
    email = serializers.EmailField(allow_blank=False)
    username = serializers.CharField(allow_blank=False, max_length=50)
    password = serializers.CharField(allow_blank=False, max_length=50)
    password_check = serializers.CharField(allow_blank=False, max_length=50)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate(self, attrs):
        """Проверка email, username, пароля."""
        username = attrs['username']
        email = attrs['email']
        password = attrs['password']
        password_check = attrs['password_check']
        if password != password_check:
            raise serializers.ValidationError(PASSWORD_ERROR,)
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(USERNAME_UNIQUE,)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(EMAIL_UNIQUE,)
        return attrs


class CodeSerializerForAuth(serializers.Serializer):
    """Сериализатор для подтверждения регистрации."""
    email = serializers.EmailField(allow_blank=False)
    confirmation_code = serializers.CharField(allow_blank=False)


class UserSerializerForAdmin(serializers.ModelSerializer):
    """Сериализатор для Администратора."""
    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email',
                  'photo', 'last_login', 'status', 'is_superuser',)
        model = User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для Пользователя."""
    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'email', 'photo',)
        model = User
