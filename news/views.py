from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, SAFE_METHODS, )

from api_news.settings import EMAIL_HOST_USER
from .filters import NewsFilter
from .models import Category, Comment, News
from .permissions import IsAdmin, IsAuthorOrAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          NewsSerializer, NewsPostSerializer)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().annotate(
        comment=Count('comments__news')
    ).prefetch_related('category').order_by('-pub_date')
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NewsFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return NewsSerializer
        return NewsPostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,
                          IsAuthorOrAdminOrReadOnly)

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        return Comment.objects.filter(
            news=news_id
        ).prefetch_related('news', 'author')

    def perform_create(self, serializer, *args, **kwargs):
        news_id = self.kwargs['news_id']
        news = get_object_or_404(News, id=news_id)
        if 'parent' in serializer.validated_data.keys():
            self.email_about_comment(serializer)
        serializer.save(author=self.request.user, news=news)

    def perform_update(self, serializer):
        if 'parent' in serializer.validated_data.keys():
            self.email_about_comment(serializer)
        serializer.save()

    def email_about_comment(self, serializer):
        user = serializer.validated_data['parent'].author
        send_mail(subject='Comment for you :)',
                  message=('К твоему коментарию пользователь '
                           f'{self.request.user.username} оставил свой '
                           'комментарий, иди скорее читай'),
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email],
                  fail_silently=False)
