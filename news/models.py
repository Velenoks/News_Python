from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class News(models.Model):
    heading = models.CharField(max_length=200,
                               verbose_name='Заголовок',
                               blank=True,)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, )
    text = models.TextField(verbose_name='Текст новости',)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


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
