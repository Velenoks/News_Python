from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import AdminOnlyPermission, AdminOrAuthorPermission
from .serializers import UserSerializer


USER_DOES_NOT_EXIST = ('Ошибка при отправке запроса: '
                       'такого пользователя нет в базе данных')
FROM_EMAIL = 'api@yamdb.ru'


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
    serializer.save(last_login=None, is_active=False)
    user = User.objects.get_or_create(
        email=serializer.validated_data['email'],
        username=serializer.validated_data['username']
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
    confirmation_code = request.data['confirmation_code']
    user = get_object_or_404(User, email=email)
    if user and default_token_generator.check_token(user, confirmation_code):
        tokens = RefreshToken.for_user(user)
        data = {
            'refresh': str(tokens),
            'access': str(tokens.access_token)
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(USER_DOES_NOT_EXIST, status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnlyPermission,)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[AdminOrAuthorPermission]
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
            return Response(serializer.data)
        raise Exception('Not implemented')
