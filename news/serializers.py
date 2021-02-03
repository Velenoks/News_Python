from rest_framework import serializers

from .models import Category, Comment, News


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для Комментриев."""
    class Meta:
        exclude = ('id',)
        model = Category


class NewsSerializer(serializers.ModelSerializer):
    """Сериализатор для Новостей, Safe Methods."""
    category = CategorySerializer(required=False)
    comment = serializers.IntegerField(read_only=True, )

    class Meta:
        fields = '__all__'
        model = News


class NewsPostSerializer(serializers.ModelSerializer):
    """Сериализатор для Новостей, don't Safe Methods."""
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        fields = '__all__'
        model = News


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для Комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'parent')
        model = Comment
