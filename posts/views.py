from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Category


def home(request):
    posts = Post.objects.filter(status="published").select_related("author", "category")
    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query))
    category_slug = request.GET.get("category")
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "posts/home.html", {
        "page_obj": page_obj, "categories": Category.objects.all(), "query": query,
        "active_category": category_slug,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author", "category"), slug=slug, status="published")
    comments = post.comments.filter(approved=True)
    form = CommentForm()
    return render(request, "posts/post_detail.html", {"post": post, "comments": comments, "form": form})


@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, "Thanks! Your comment is awaiting moderation.")
    else:
        messages.error(request, "Please check your comment details.")
    return redirect("post_detail", slug=slug)


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Welcome! Your account has been created.")
        return redirect("dashboard")
    return render(request, "posts/register.html", {"form": form})


@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "posts/dashboard.html", {"posts": posts})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your post has been saved.")
        return redirect("dashboard")
    return render(request, "posts/post_form.html", {"form": form, "heading": "Write a new post"})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, "Your post has been updated.")
        return redirect("dashboard")
    return render(request, "posts/post_form.html", {"form": form, "heading": "Edit post"})


@login_required
@require_POST
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    messages.success(request, "Post deleted.")
    return redirect("dashboard")
