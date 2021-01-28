from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, \
    TokenObtainPairView

# from .views import UserViewSet, auth, get_token


router = DefaultRouter()

urlpatterns = [
    # path('v1/auth/email/', csrf_exempt(auth)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('v1/auth/token/', get_token, name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
