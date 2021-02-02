import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = os.environ.get("ADMIN_USERNAME", "admin")
            email = os.environ.get("ADMIN_EMAIL", "admin@newspy.com")
            password = os.environ.get("ADMIN_PASSWORD", "admin")
            admin = User.objects.create(email=email,
                                        username=username,
                                        password=password, )
            admin.set_password(admin.password)
            admin.is_active = True
            admin.is_superuser = True
            admin.save()
            print('Создан аккаунт для %s (%s)' % (username, email))
            u = User.objects.get(username=username)
        else:
            print('Учетная запись создается только, если нет других записей')
