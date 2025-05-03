from django.db import models


class PublishedModel(models.Model):
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
        db_index=True
    )
    is_published = models.BooleanField(
        'Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True,
        blank=False
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
