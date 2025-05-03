from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).order_by('-pub_date')

    def latest_published(self, count=5):
        return self.published()[:count]

    def with_related(self):
        return self.select_related('category', 'location', 'author')
