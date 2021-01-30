from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api_news.settings import FROM_EMAIL


schema_view = get_schema_view(
    openapi.Info(
        title='API для новостного портала',
        default_version='v1',
        description=('API с возможностью регистрации пользователей,'
                     'создание новостей и коментариев к ним'),
        contact=openapi.Contact(email=FROM_EMAIL),
        license=openapi.License(name='BSD-3-Clause License')
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)
