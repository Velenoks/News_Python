from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_news.settings import FROM_EMAIL
from .models import User
from .permissions import AdminOnlyPermission, AdminOrAuthorPermission
from .serializers import UserSerializer, UserSerializerForAdmin

USER_DOES_NOT_EXIST = ('Ошибка при отправке запроса: '
                       'такого пользователя нет в базе данных')
PASSWORD_ERROR = 'Пароли не совпадают'


@api_view(['POST'])
@permission_classes([AllowAny])
def auth(request):
    email = request.data['email']
    username = email[0:email.find('@')]
    serializer = UserSerializer(
        data={
            'email': email,
            'username': username
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save(last_login=None)
    user = User.objects.get_or_create(
        email=serializer.validated_data['email'],
        username=serializer.validated_data['username'],
    )
    confirmation_code = default_token_generator.make_token(user[0])
    send_mail(
        subject='Confirmation Code',
        message=('Код подтверждения для получения токена: '
                 f'{confirmation_code}'),
        from_email=FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    email = request.data['email']
    user = get_object_or_404(User, email=email)
    confirmation_code = request.data['confirmation_code']
    password = request.data['password']
    password_check = request.data['password_check']
    if password != password_check:
        return Response(PASSWORD_ERROR, status.HTTP_400_BAD_REQUEST)
    if user and default_token_generator.check_token(user, confirmation_code):
        user.password = make_password(password)
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

    def get_object(self):
        user = get_object_or_404(User, username=self.kwargs['pk'])
        return user

    def perform_update(self, serializer, *args, **kwargs):
        username = self.kwargs['pk']
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

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(AdminOrAuthorPermission,)
    )
    def me(self, request):
        self.kwargs['pk'] = request.user.username
        if request.method == 'GET':
            return self.retrieve(request)
        elif request.method == 'PATCH':
            instance = self.get_object()
            serializer = UserSerializer(
                instance,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise Exception('Not implemented')
