from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news.urls',
                         namespace='news')),
    path('api/', include('users.urls',
                         namespace='users-api')),
]
