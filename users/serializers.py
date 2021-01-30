from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'photo',
            'last_login',
            'is_active',
        )
        model = User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'photo',
        )
        model = User
