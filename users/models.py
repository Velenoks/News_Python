from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True,
                              db_index=True,
                              verbose_name='Электронная почта')
    username = models.CharField(max_length=150,
                                unique=True,
                                blank=False,
                                verbose_name='Имя пользователе')

    class Meta:
        ordering = ['-id']
