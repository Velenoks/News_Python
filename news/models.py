from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Категория',
                            blank=True,)
    slug = models.SlugField(unique=True,
                            verbose_name='Slug',)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class News(models.Model):
    heading = models.CharField(max_length=200,
                               verbose_name='Заголовок',
                               blank=True,)
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True,)
    text = models.TextField(verbose_name='Текст новости',)
    category = models.ForeignKey(Category,
                                 blank=True,
                                 default='Без категории',
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name='Категория',
                                 related_name='titles')
    image = models.ImageField(upload_to='posts/',
                              verbose_name='Картинка',
                              blank=True,)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.heading


class Comment(models.Model):
    news = models.ForeignKey(News,
                             verbose_name='Новость',
                             on_delete=models.CASCADE,
                             related_name='comments',)
    text = models.TextField(verbose_name='Текст коментария',)
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments',)
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
