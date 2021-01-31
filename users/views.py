from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_news.settings import FROM_EMAIL
from .models import User
from .permissions import AdminOnlyPermission, AdminOrAuthorPermission
from .serializers import (UserSerializer, UserSerializerForAdmin,
                          UserSerializerForAuth, CodeSerializerForAuth, )


USER_DOES_NOT_EXIST = ('Ошибка при отправке запроса: '
                       'такого пользователя нет в базе данных')


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    serializer = UserSerializerForAuth(data=request.data)
    serializer.is_valid(raise_exception=True)
    del serializer.validated_data['password_check']
    serializer.save(last_login=None, is_active=False)
    user = User.objects.get(
        email=serializer.validated_data['email'],
        username=serializer.validated_data['username'],
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(subject='Confirmation Code',
              message=('Код подтверждения для получения токена: '
                       f'{confirmation_code}'),
              from_email=FROM_EMAIL,
              recipient_list=[user.email],
              fail_silently=False, )
    return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = CodeSerializerForAuth(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    user = get_object_or_404(User, email=email)
    confirmation_code = serializer.validated_data['confirmation_code']
    if user and default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        tokens = RefreshToken.for_user(user)
        data = {
            'access': str(tokens.access_token),
            'refresh': str(tokens),
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(USER_DOES_NOT_EXIST, status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    permission_classes = (AdminOnlyPermission,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    def perform_update(self, serializer, *args, **kwargs):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        if 'status' in serializer.validated_data.keys():
            if serializer.validated_data['status'] == 'mute':
                send_mail(subject='Status MUTE :(',
                          message=('Нам пришлось ограчить вашу возможность '
                                   'оставлять комментарии, вы нарушили '
                                   'правила размещения коментариев.'),
                          from_email=FROM_EMAIL,
                          recipient_list=[user.email],
                          fail_silently=False)
            elif serializer.validated_data['status'] == 'user':
                send_mail(subject='Status USER :)',
                          message=('Поздравляю, вы можете снова оставлять  '
                                   'комментарии к новостям!'),
                          from_email=FROM_EMAIL,
                          recipient_list=[user.email],
                          fail_silently=False)
        serializer.save()


class UserMeViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = UserSerializer
    permission_classes = (AdminOrAuthorPermission,)
    lookup_field = 'username'

    def get_object(self):
        return User.objects.get(username=self.request.user.username)
