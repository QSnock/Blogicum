from django.db import models


class CreatedModel(models.Model):
    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class PublishedModel(CreatedModel):
    is_published = models.BooleanField(
        'Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        default=True,
        blank=False
    )

    class Meta(CreatedModel.Meta):
        abstract = True
