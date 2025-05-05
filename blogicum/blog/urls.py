from django.urls import path, include

from . import views

app_name = 'blog'

# Посты.
post_endpoints = [
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path(
        '<int:post_id>/edit/',
        views.PostEditView.as_view(),
        name='edit_post'
    ),
    path(
        '<int:post_id>/delete/',
        views.PostDeleteView.as_view(),
        name='delete_post'
    ),
]

# Комментарии.
comment_endpoints = [
    path('<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path(
        '<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment'
    ),
    path(
        '<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment'
    ),
]

# Профиль.
profile_endpoints = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('<str:username>/', views.profile, name='profile'),
]

# Аутентификация.
auth_endpoints = [
    path(
        'registration/',
        views.RegistrationView.as_view(),
        name='registration'
    ),
    path('logout/', views.logout_page, name='logout'),
]

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', include(profile_endpoints)),
    path('posts/', include(post_endpoints)),
    path('posts/', include(comment_endpoints)),
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    path('auth/', include(auth_endpoints)),
]
