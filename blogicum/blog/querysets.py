from django.db import models
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import get_object_or_404


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        ).order_by('-pub_date')

    def with_comments_count(self):
        return self.annotate(comment_count=Count('comments'))

    def latest_published(self, count=5):
        return self.published()[:count]

    def with_related(self):
        return self.select_related('category', 'location', 'author')

    def get_post_with_related(self, post_id):
        return get_object_or_404(
            self.with_related(),
            pk=post_id
        )
