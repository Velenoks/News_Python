from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'news'

router = DefaultRouter()
router.register(r'categories',
                views.CategoryViewSet,
                basename=app_name)
router.register(r'news',
                views.TitleViewSet,
                basename=app_name)
router.register(r'news/(?P<news_id>\d+)/comments',
                views.ReviewViewSet,
                basename=app_name)

urlpatterns = [
    path('v1/', include(router.urls)),
]