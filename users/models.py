from django.contrib.auth.models import AbstractUser
from django.db import models


class UserStatus(models.TextChoices):
    MUTE = 'mute'
    USER = 'user'


class User(AbstractUser):
    email = models.EmailField(unique=True,
                              db_index=True,
                              verbose_name='Электронная почта')
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                verbose_name='Имя пользователе')
    photo = models.ImageField(upload_to='users/',
                              verbose_name='Фото',
                              blank=True, )
    status = models.CharField(max_length=10,
                              blank=False,
                              choices=UserStatus.choices,
                              default=UserStatus.USER,
                              verbose_name='Статус пользователя')

    class Meta:
        ordering = ['-id']
