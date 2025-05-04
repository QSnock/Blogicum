from django.core.paginator import Paginator

POST_TITLE_MAX_LENGTH = 256
POST_PUB_DATE_HELP_TEXT = (
    'Если установить дату и время в будущем — '
    'можно делать отложенные публикации.'
)

CATEGORY_TITLE_MAX_LENGTH = 256
CATEGORY_SLUG_HELP_TEXT = (
    'Идентификатор страницы для URL; '
    'разрешены символы латиницы, цифры, дефис и подчёркивание.'
)

LOCATION_NAME_MAX_LENGTH = 256


def get_paginated_posts(queryset, request, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
