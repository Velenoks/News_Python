# Generated by Django 3.1.5 on 2021-01-30 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('admin', 'Admin'), ('mute', 'Mute'), ('user', 'User')], default='user', max_length=10, verbose_name='Статус пользователя'),
        ),
    ]
