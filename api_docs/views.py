from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api_news.settings import FROM_EMAIL

schema_view = get_schema_view(
    openapi.Info(
        title='API для новостного портала',
        default_version='v1',
        description=(
            'Pапросы к API начинаются с `/api/v1/`\n\n'
            '**Описание**\n'
            'Данное API разработанно для новостного портала с возможностью регистрации пользователей, просмотра новостей и коментариев к ним.\n\n'
            '**Алгоритм регистрации пользователей**\n'
            '1. Пользователь отправляет запрос с параметром `email`, `username`, `password`, `password_check` на `/auth/email/`.\n\n'
            '2. Приложение отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email` .\n\n'
            '3. Пользователь отправляет запрос с параметрами `email` и `confirmation_code` на `/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).\n Пока пользователь не подтвердит регистрацию через `confirmation_code`, он не сможет пользоваться ресурсом. \n\n'
            '4. При желании пользователь отправляет PATCH-запрос на `/users/me/username` и заполняет поля в своём профайле (описание полей — в документации).\n\n'
            '**Пользовательские роли**\n'
            '- **Аноним** — может просматривать новости, но невидит и не может оставлять комментарии.\n'
            '- **Аутентифицированный пользователь** — может читать новости, может читать и оставлять коментарии, комментировать чужие коментарии, может редактировать и удалять **свои** комментарии.\n'
            '- **Заблокированный пользователь** — те же права, что и у **Аутентифицированного пользователя**, но отсуствует возможность писать и редактировать комментарии.\n '
            '- **Администратор** — полные права на управление проектом и всем его содержимым. Может создавать и удалять новости и комментарии. Может назначать роли пользователям.\n\n'
            '**Создание Администратора**\n'
            'Приложение иметь возможность создавать администратора запуском команды из консоли `python manage.py createsuperuser`.\n'
            'Так же любой Администратор может назначить любого пользователя Администратором. \n'
        ),
        contact=openapi.Contact(email=FROM_EMAIL),
        license=openapi.License(name='BSD-3-Clause License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
