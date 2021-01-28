from rest_framework import serializers

from .models import Category, Comment, News


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category


class NewsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False)
    comment = serializers.IntegerField(read_only=True, )

    class Meta:
        fields = '__all__'
        model = News


class NewsPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        fields = '__all__'
        model = News


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'parent')
        model = Comment
