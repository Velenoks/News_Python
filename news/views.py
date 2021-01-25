from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import NewsFilter
from .models import Category, Comment, News
from .permissions import IsAdmin, IsAuthorOrAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          NewsSerializer)


class CategoryViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdmin,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsFilter

    def perform_create(self, serializer):
        data = self.request.data
        category_slug = data['category']
        category = get_object_or_404(Category, slug=category_slug,)
        serializer.save(category=category,)

    def perform_update(self, serializer):
        category_slug = self.request.data['category']
        category = get_object_or_404(Category, slug=category_slug,)
        serializer.save(category=category,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrReadOnly)

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        return Comment.objects.filter(news=news_id)

    def perform_create(self, serializer, *args, **kwargs):
        news_id = self.kwargs['news_id']
        news = get_object_or_404(News, id=news_id)
        serializer.save(author=self.request.user, news=news)
