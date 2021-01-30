from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('news.urls', namespace='news')),
    path('api/', include(('users.urls', 'users'), namespace='users-api')),
    path('', include(('api_docs.urls', 'api_docs'), namespace='docs')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
