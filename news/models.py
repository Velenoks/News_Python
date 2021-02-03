from django.contrib.auth import get_user_model
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()


class Category(models.Model):
    """Модель для Категорий."""
    name = models.CharField(max_length=200,
                            verbose_name='Категория',
                            blank=True, )
    slug = models.SlugField(unique=True,
                            verbose_name='Slug', )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class News(models.Model):
    """Модель для новостей."""
    heading = models.CharField(max_length=200,
                               verbose_name='Заголовок',
                               unique=True, )
    pub_date = models.DateTimeField('Дата публикации',
                                    auto_now_add=True, )
    text = models.TextField(verbose_name='Текст новости', )
    category = models.ForeignKey(Category,
                                 blank=True,
                                 default='Без категории',
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name='Категория',
                                 related_name='news')
    image = models.ImageField(upload_to='news/',
                              verbose_name='Картинка',
                              blank=True, )

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.heading


class Comment(MPTTModel):
    """Модель для Комментариев."""
    news = models.ForeignKey(News,
                             verbose_name='Новость',
                             on_delete=models.CASCADE,
                             related_name='comments', )
    text = models.TextField(verbose_name='Текст коментария', )
    author = models.ForeignKey(User,
                               verbose_name='Автор',
                               on_delete=models.CASCADE,
                               related_name='comments', )
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True, )
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True,
                            related_name='children', )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    class MPTTMeta:
        order_insertin_by = ['text']

    def save(self, *args, **kwargs):  # Проверка на максимальную вложенность
        if self.parent is not None and self.parent.level == 5:
            raise ValueError(u'Достигнута максимальная вложенность!')
        super(Comment, self).save(*args, **kwargs)
