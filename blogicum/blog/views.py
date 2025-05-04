from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from .models import Post, Category, Comment
from .forms import RegistrationForm, CommentForm, ProfileEditForm
from .constants import get_paginated_posts

User = get_user_model()


def index(request):
    post_list = Post.objects.published().with_comments_count()
    return render(request, 'blog/index.html', {
        'page_obj': get_paginated_posts(post_list, request)
    })


def post_detail(request, post_id):
    post = Post.objects.get_post_with_related(post_id)

    is_visible = (
        Post.objects.published().filter(pk=post_id).exists()
        or post.author == request.user
    )

    if not is_visible:
        return render(request, 'pages/404.html', status=404)

    comments = post.comments.order_by('created_at')
    form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('blog:post_detail', post_id=post.id)


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        pk=comment_id,
        author=request.user,
        post_id=post_id
    )
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {
        'form': CommentForm(instance=comment),
        'comment': comment,
        'post': comment.post
    })


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        author=request.user,
        post_id=post_id
    )
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {
        'comment': comment,
        'post': comment.post
    })


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.published().with_comments_count()

    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': get_paginated_posts(posts, request)
    })


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
    success_url = reverse_lazy('login')


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    posts = profile.posts.with_comments_count().order_by('-pub_date')

    if request.user != profile:
        posts = posts.published()

    return render(request, 'blog/profile.html', {
        'profile': profile,
        'page_obj': get_paginated_posts(posts, request)
    })


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'registration/logged_out.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/user.html', {
        'form': ProfileEditForm(instance=request.user)
    })


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'pub_date', 'location', 'category', 'image']
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'
    queryset = Post.objects.with_related()

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', post_id=self.get_object().pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username}
        )
