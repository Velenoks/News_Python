from django.urls import path

from .views import schema_view

urlpatterns = [
    path(r'swagger/',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui', ),
    path(r'redoc/',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc', ),
]
