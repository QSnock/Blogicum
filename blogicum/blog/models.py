from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel, CreatedModel
from .querysets import PostQuerySet
from .constants import (
    POST_TITLE_MAX_LENGTH,
    POST_PUB_DATE_HELP_TEXT,
    CATEGORY_TITLE_MAX_LENGTH,
    CATEGORY_SLUG_HELP_TEXT,
    LOCATION_NAME_MAX_LENGTH
)

User = get_user_model()


class Post(PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=POST_TITLE_MAX_LENGTH,
        blank=False
    )
    text = models.TextField('Текст', blank=False)
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=POST_PUB_DATE_HELP_TEXT,
        blank=False
    )
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='posts_images/',
        blank=True,
        null=True,
    )
    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        default_related_name = 'posts'

    def __str__(self):
        return self.title


class Category(PublishedModel):
    title = models.CharField(
        'Заголовок',
        max_length=CATEGORY_TITLE_MAX_LENGTH,
        blank=False
    )
    description = models.TextField('Описание', blank=False)
    slug = models.SlugField(
        'Идентификатор',
        help_text=CATEGORY_SLUG_HELP_TEXT,
        unique=True,
        blank=False
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'

    def __str__(self):
        return self.title


class Location(PublishedModel):
    name = models.CharField(
        'Название места',
        max_length=LOCATION_NAME_MAX_LENGTH,
        blank=False
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        default_related_name = 'locations'

    def __str__(self):
        return self.name


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Публикация'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField('Текст комментария')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий {self.author} к посту {self.post.id}'
