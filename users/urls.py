from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView,
                                            TokenObtainPairView)

from .views import UserViewSet, auth, get_token


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/email/', csrf_exempt(auth)),
    path('v1/auth/token/', get_token, name='token_new_user'),
    path('v1/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/', include(router.urls)),
]
